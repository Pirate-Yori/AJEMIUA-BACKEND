# users/views.py

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from django.conf import settings
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
import pandas as pd
import io
from datetime import datetime

from .permissions import IsAdminUserCustom
from .serializers import AdminLoginSerializer

from . import serializers
from .models import CustomUser

User = get_user_model()

# L'inscription publique a été supprimée - seuls les admins peuvent créer des utilisateurs

class UserLoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        # Vérifier si l'utilisateur est actif (is_member)
        if not user.is_member:
            return Response(
                {"detail": "Votre compte a été désactivé. Veuillez contacter l'administrateur."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Génération des tokens
        token = RefreshToken.for_user(user)

        data = serializers.CustomUserSerializer(user).data
        data["tokens"] = {
            "refresh": str(token),
            "access": str(token.access_token),
        }
        
        # Informer si le mot de passe doit être changé
        if not user.password_changed:
            data["password_change_required"] = True
            data["message"] = "Vous devez changer votre mot de passe à la première connexion."

        return Response(data, status=status.HTTP_200_OK)


class UserLogoutAPIView(GenericAPIView):
    """
    An endpoint to logout users.
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(RetrieveUpdateAPIView):
    """
    Get, Update user information
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CustomUserSerializer

    def get_object(self):
        return self.request.user



class AdminLoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = AdminLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token = RefreshToken.for_user(user)

        return Response({
            "admin": serializers.CustomUserSerializer(user).data,
            "tokens": {
                "refresh": str(token),
                "access": str(token.access_token)
            }
        })



class AdminUserListAPIView(ListAPIView):
    """
    Liste tous les utilisateurs (pour l'admin)
    """
    permission_classes = [IsAuthenticated, IsAdminUserCustom]
    serializer_class = serializers.AdminUserSerializer
    
    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')







class UserDetailAPIView(RetrieveUpdateAPIView):
    """
    Voir et modifier les détails d'un utilisateur spécifique (pour l'admin)
    """
    permission_classes = [IsAuthenticated, IsAdminUserCustom]
    serializer_class = serializers.AdminUserSerializer
    queryset = User.objects.all()
    lookup_field = 'id'


class ImportUsersFromExcelAPIView(APIView):
    """
    Importe des utilisateurs depuis un fichier Excel
    Format Excel attendu: matricule, nom, prenom, telephone
    """
    permission_classes = [IsAuthenticated, IsAdminUserCustom]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, *args, **kwargs):
        # Vérifier que le fichier est présent
        if 'file' not in request.FILES:
            return Response(
                {
                    "detail": "Aucun fichier fourni.",
                    "instructions": "Utilisez 'form-data' dans Postman avec la clé 'file' de type File"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        excel_file = request.FILES['file']
        
        # Vérifier l'extension du fichier
        if not excel_file.name.endswith(('.xlsx', '.xls')):
            return Response(
                {
                    "detail": "Le fichier doit être un fichier Excel (.xlsx ou .xls)",
                    "fichier_recu": excel_file.name
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        default_password = request.data.get('default_password', 'Etudiant123')  # Mot de passe par défaut
        
        try:
            # Lire le fichier Excel
            df = pd.read_excel(excel_file)
            
            # Vérifier que le DataFrame n'est pas vide
            if df.empty:
                return Response(
                    {"detail": "Le fichier Excel est vide."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Vérifier les colonnes requises
            required_columns = ['matricule', 'nom', 'prenom', 'telephone']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return Response(
                    {
                        "detail": f"Colonnes manquantes dans le fichier Excel: {', '.join(missing_columns)}",
                        "colonnes_requises": required_columns,
                        "colonnes_trouvees": list(df.columns)
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Récupérer le rôle "étudiant"
            from api.models import Role
            etudiant_role, _ = Role.objects.get_or_create(type="étudiant")
            
            created_users_data = []
            errors = []
            
            for index, row in df.iterrows():
                try:
                    matricule = str(row['matricule']).strip()
                    nom = str(row['nom']).strip()
                    prenom = str(row['prenom']).strip()
                    telephone = str(row['telephone']).strip()
                    
                    # Vérifier si l'utilisateur existe déjà
                    if User.objects.filter(matricule=matricule).exists():
                        errors.append(f"Ligne {index + 2}: Matricule {matricule} existe déjà")
                        continue
                    
                    # Créer l'utilisateur avec le mot de passe par défaut
                    user = User.objects.create_user(
                        matricule=matricule,
                        nom=nom,
                        prenom=prenom,
                        telephone=telephone,
                        password=default_password
                    )
                    
                    # Assigner le rôle étudiant
                    user.roles.add(etudiant_role)
                    # is_member = True par défaut (utilisateur actif)
                    # password_changed reste False pour forcer le changement à la première connexion
                    
                    # Stocker les données pour le fichier Excel de retour
                    created_users_data.append({
                        "matricule": user.matricule,
                        "nom": user.nom,
                        "prenom": user.prenom,
                        "telephone": user.telephone,
                        "mot_de_passe": default_password
                    })
                    
                except Exception as e:
                    errors.append(f"Ligne {index + 2}: {str(e)}")
                    continue
            
            # Si aucun utilisateur n'a été créé, retourner une erreur
            if not created_users_data:
                return Response(
                    {
                        "detail": "Aucun utilisateur n'a été créé.",
                        "errors": errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Créer un DataFrame avec les utilisateurs créés et leurs mots de passe
            result_df = pd.DataFrame(created_users_data)
            
            # Créer un fichier Excel en mémoire
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                result_df.to_excel(writer, index=False, sheet_name='Utilisateurs_Créés')
                
                # Ajouter une feuille d'erreurs si nécessaire
                if errors:
                    errors_df = pd.DataFrame({
                        'Erreurs': errors
                    })
                    errors_df.to_excel(writer, index=False, sheet_name='Erreurs')
            
            output.seek(0)
            
            # Préparer le nom du fichier avec la date
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"utilisateurs_crees_{timestamp}.xlsx"
            
            # Retourner le fichier Excel
            response = HttpResponse(
                output.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            
            return response
            
        except pd.errors.EmptyDataError:
            return Response(
                {"detail": "Le fichier Excel est vide ou ne contient pas de données."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except pd.errors.ExcelFileError as e:
            return Response(
                {
                    "detail": "Erreur lors de la lecture du fichier Excel.",
                    "erreur": str(e),
                    "instructions": "Assurez-vous que le fichier est un fichier Excel valide (.xlsx ou .xls)"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            import traceback
            return Response(
                {
                    "detail": f"Erreur lors du traitement du fichier Excel: {str(e)}",
                    "type_erreur": type(e).__name__,
                    "traceback": traceback.format_exc() if settings.DEBUG else None
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class ChangePasswordAPIView(APIView):
    """
    Permet à un utilisateur de changer son mot de passe
    Si password_changed=False, c'est obligatoire à la première connexion
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response(
                {"detail": "Les champs 'old_password' et 'new_password' sont requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = request.user
        
        # Vérifier l'ancien mot de passe
        if not user.check_password(old_password):
            return Response(
                {"detail": "Ancien mot de passe incorrect."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier que le nouveau mot de passe est différent
        if user.check_password(new_password):
            return Response(
                {"detail": "Le nouveau mot de passe doit être différent de l'ancien."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Changer le mot de passe
        user.set_password(new_password)
        user.password_changed = True
        user.save()
        
        return Response(
            {"message": "Mot de passe changé avec succès."},
            status=status.HTTP_200_OK
        )






