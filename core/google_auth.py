import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import usuarios

class GoogleLoginView(APIView):
    def post(self, request):
        # 1. Recibimos el token que nos manda el frontend (Expo)
        google_token = request.data.get('token')
        if not google_token:
            return Response({'error': 'Token de Google no proporcionado'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Django le pregunta a Google: "¿Este token es válido?"
        try:
            # Esta es la URL oficial de Google para verificar tokens
            response = requests.get(f'https://www.googleapis.com/oauth2/v2/userinfo?access_token={google_token}')
            data = response.json()
            
            # Si Google responde con error, el token es falso o expiró
            if 'error' in data:
                return Response({'error': 'Token de Google inválido'}, status=status.HTTP_401_UNAUTHORIZED)
            
            # 3. Extraemos la info del usuario que nos da Google
            google_uid = data.get('sub')
            email = data.get('email')
            first_name = data.get('given_name', '')
            last_name = data.get('family_name', '')
            picture = data.get('picture', '')

        except Exception as e:
            return Response({'error': 'Error al conectar con Google'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 4. Lógica de nuestra base de datos: ¿Existe el usuario?
        user = None
        
        # Primero buscamos por el UID exacto de Google (Lo más seguro)
        if google_uid:
            user = usuarios.objects.filter(google_uid=google_uid).first()
            
        # Si no existe por UID, buscamos por correo (Por si se registró por otro método antes)
        if not user and email:
            user = usuarios.objects.filter(email=email).first()
            # Si lo encuentra por email, le ligamos su Google UID para futuros logins
            if user:
                user.google_uid = google_uid
                user.save()

        # 5. Si nunca ha existido, LO CREAMOS
        if not user:
            # Generamos un username basado en su correo (Django lo exige)
            username = email.split('@')[0]
            # Evitamos duplicados de username
            base_username = username
            counter = 1
            while usuarios.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            user = usuarios.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                google_uid=google_uid,
                role='cliente', # Por defecto, alguien que se registra con Google es cliente
                is_active=True
            )
            # Opcional: Descargar la imagen de Google y guardarla en tu campo 'imagen'

        # 6. Generamos los JWT (Las llaves de acceso de la app)
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login exitoso',
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
                'role': user.role
            }
        }, status=status.HTTP_200_OK)