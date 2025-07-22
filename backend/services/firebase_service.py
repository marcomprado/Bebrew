"""
Serviço do Firebase para Bebrew
"""
import firebase_admin
from firebase_admin import credentials, firestore, auth
from typing import Dict, List, Optional, Any
from loguru import logger
from ..config.settings import get_settings


class FirebaseService:
    """Serviço para integração com Firebase"""
    
    def __init__(self):
        self.settings = get_settings()
        self._initialize_firebase()
        self.db = firestore.client()
        
    def _initialize_firebase(self):
        """Inicializa o Firebase Admin SDK"""
        try:
            # Configuração das credenciais
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": self.settings.firebase_project_id,
                "private_key_id": self.settings.firebase_private_key_id,
                "private_key": self.settings.firebase_private_key.replace('\\n', '\n'),
                "client_email": self.settings.firebase_client_email,
                "client_id": self.settings.firebase_client_id,
                "auth_uri": self.settings.firebase_auth_uri,
                "token_uri": self.settings.firebase_token_uri,
                "auth_provider_x509_cert_url": self.settings.firebase_auth_provider_x509_cert_url,
                "client_x509_cert_url": self.settings.firebase_client_x509_cert_url
            })
            
            # Inicializa o app se não existir
            if not firebase_admin._apps:
                firebase_admin.initialize_app(cred)
                
            logger.info("Firebase inicializado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar Firebase: {e}")
            raise
    
    # Métodos de Autenticação
    async def create_user(self, email: str, password: str, display_name: str = None) -> Dict[str, Any]:
        """
        Cria um novo usuário no Firebase Auth
        
        Args:
            email: Email do usuário
            password: Senha do usuário
            display_name: Nome de exibição (opcional)
            
        Returns:
            Dados do usuário criado
        """
        try:
            user_properties = {
                'email': email,
                'password': password,
                'email_verified': False
            }
            
            if display_name:
                user_properties['display_name'] = display_name
            
            user = auth.create_user(**user_properties)
            
            # Cria documento do usuário no Firestore
            await self._create_user_document(user.uid, {
                'email': email,
                'display_name': display_name,
                'created_at': firestore.SERVER_TIMESTAMP,
                'profile': {
                    'experience_level': 'beginner',
                    'preferred_styles': [],
                    'equipment': []
                }
            })
            
            return {
                'uid': user.uid,
                'email': user.email,
                'display_name': user.display_name,
                'created_at': user.user_metadata.creation_timestamp
            }
            
        except Exception as e:
            logger.error(f"Erro ao criar usuário: {e}")
            raise
    
    async def verify_token(self, id_token: str) -> Dict[str, Any]:
        """
        Verifica um token de autenticação
        
        Args:
            id_token: Token JWT do Firebase
            
        Returns:
            Dados do usuário autenticado
        """
        try:
            decoded_token = auth.verify_id_token(id_token)
            return {
                'uid': decoded_token['uid'],
                'email': decoded_token.get('email'),
                'email_verified': decoded_token.get('email_verified', False)
            }
            
        except Exception as e:
            logger.error(f"Erro ao verificar token: {e}")
            raise
    
    # Métodos de Receitas
    async def save_recipe(self, user_id: str, recipe_data: Dict[str, Any]) -> str:
        """
        Salva uma receita no Firestore
        
        Args:
            user_id: ID do usuário
            recipe_data: Dados da receita
            
        Returns:
            ID da receita criada
        """
        try:
            recipe_ref = self.db.collection('users').document(user_id).collection('recipes')
            
            # Adiciona metadados
            recipe_data['created_at'] = firestore.SERVER_TIMESTAMP
            recipe_data['updated_at'] = firestore.SERVER_TIMESTAMP
            recipe_data['user_id'] = user_id
            
            doc_ref = recipe_ref.add(recipe_data)[1]
            
            logger.info(f"Receita salva com ID: {doc_ref.id}")
            return doc_ref.id
            
        except Exception as e:
            logger.error(f"Erro ao salvar receita: {e}")
            raise
    
    async def get_user_recipes(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Obtém todas as receitas de um usuário
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Lista de receitas
        """
        try:
            recipes_ref = self.db.collection('users').document(user_id).collection('recipes')
            docs = recipes_ref.order_by('created_at', direction=firestore.Query.DESCENDING).stream()
            
            recipes = []
            for doc in docs:
                recipe_data = doc.to_dict()
                recipe_data['id'] = doc.id
                recipes.append(recipe_data)
            
            return recipes
            
        except Exception as e:
            logger.error(f"Erro ao obter receitas: {e}")
            raise
    
    async def get_recipe(self, user_id: str, recipe_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtém uma receita específica
        
        Args:
            user_id: ID do usuário
            recipe_id: ID da receita
            
        Returns:
            Dados da receita ou None
        """
        try:
            doc_ref = self.db.collection('users').document(user_id).collection('recipes').document(recipe_id)
            doc = doc_ref.get()
            
            if doc.exists:
                recipe_data = doc.to_dict()
                recipe_data['id'] = doc.id
                return recipe_data
            else:
                return None
                
        except Exception as e:
            logger.error(f"Erro ao obter receita: {e}")
            raise
    
    async def update_recipe(self, user_id: str, recipe_id: str, recipe_data: Dict[str, Any]) -> bool:
        """
        Atualiza uma receita
        
        Args:
            user_id: ID do usuário
            recipe_id: ID da receita
            recipe_data: Novos dados da receita
            
        Returns:
            True se atualizado com sucesso
        """
        try:
            recipe_data['updated_at'] = firestore.SERVER_TIMESTAMP
            
            doc_ref = self.db.collection('users').document(user_id).collection('recipes').document(recipe_id)
            doc_ref.update(recipe_data)
            
            logger.info(f"Receita {recipe_id} atualizada com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao atualizar receita: {e}")
            raise
    
    async def delete_recipe(self, user_id: str, recipe_id: str) -> bool:
        """
        Deleta uma receita
        
        Args:
            user_id: ID do usuário
            recipe_id: ID da receita
            
        Returns:
            True se deletado com sucesso
        """
        try:
            doc_ref = self.db.collection('users').document(user_id).collection('recipes').document(recipe_id)
            doc_ref.delete()
            
            logger.info(f"Receita {recipe_id} deletada com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao deletar receita: {e}")
            raise
    
    # Métodos de Produção
    async def save_production(self, user_id: str, production_data: Dict[str, Any]) -> str:
        """
        Salva dados de produção
        
        Args:
            user_id: ID do usuário
            production_data: Dados da produção
            
        Returns:
            ID da produção criada
        """
        try:
            production_ref = self.db.collection('users').document(user_id).collection('productions')
            
            # Adiciona metadados
            production_data['created_at'] = firestore.SERVER_TIMESTAMP
            production_data['updated_at'] = firestore.SERVER_TIMESTAMP
            production_data['user_id'] = user_id
            
            doc_ref = production_ref.add(production_data)[1]
            
            logger.info(f"Produção salva com ID: {doc_ref.id}")
            return doc_ref.id
            
        except Exception as e:
            logger.error(f"Erro ao salvar produção: {e}")
            raise
    
    async def get_user_productions(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Obtém todas as produções de um usuário
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Lista de produções
        """
        try:
            productions_ref = self.db.collection('users').document(user_id).collection('productions')
            docs = productions_ref.order_by('created_at', direction=firestore.Query.DESCENDING).stream()
            
            productions = []
            for doc in docs:
                production_data = doc.to_dict()
                production_data['id'] = doc.id
                productions.append(production_data)
            
            return productions
            
        except Exception as e:
            logger.error(f"Erro ao obter produções: {e}")
            raise
    
    # Métodos de Ingredientes
    async def save_ingredient(self, user_id: str, ingredient_data: Dict[str, Any]) -> str:
        """
        Salva um ingrediente no inventário do usuário
        
        Args:
            user_id: ID do usuário
            ingredient_data: Dados do ingrediente
            
        Returns:
            ID do ingrediente criado
        """
        try:
            ingredient_ref = self.db.collection('users').document(user_id).collection('ingredients')
            
            ingredient_data['created_at'] = firestore.SERVER_TIMESTAMP
            ingredient_data['updated_at'] = firestore.SERVER_TIMESTAMP
            ingredient_data['user_id'] = user_id
            
            doc_ref = ingredient_ref.add(ingredient_data)[1]
            
            logger.info(f"Ingrediente salvo com ID: {doc_ref.id}")
            return doc_ref.id
            
        except Exception as e:
            logger.error(f"Erro ao salvar ingrediente: {e}")
            raise
    
    async def get_user_ingredients(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Obtém todos os ingredientes de um usuário
        
        Args:
            user_id: ID do usuário
            
        Returns:
            Lista de ingredientes
        """
        try:
            ingredients_ref = self.db.collection('users').document(user_id).collection('ingredients')
            docs = ingredients_ref.stream()
            
            ingredients = []
            for doc in docs:
                ingredient_data = doc.to_dict()
                ingredient_data['id'] = doc.id
                ingredients.append(ingredient_data)
            
            return ingredients
            
        except Exception as e:
            logger.error(f"Erro ao obter ingredientes: {e}")
            raise
    
    # Métodos auxiliares
    async def _create_user_document(self, user_id: str, user_data: Dict[str, Any]):
        """Cria documento do usuário no Firestore"""
        try:
            self.db.collection('users').document(user_id).set(user_data)
            logger.info(f"Documento do usuário criado: {user_id}")
            
        except Exception as e:
            logger.error(f"Erro ao criar documento do usuário: {e}")
            raise
    
    async def update_user_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """
        Atualiza o perfil do usuário
        
        Args:
            user_id: ID do usuário
            profile_data: Novos dados do perfil
            
        Returns:
            True se atualizado com sucesso
        """
        try:
            profile_data['updated_at'] = firestore.SERVER_TIMESTAMP
            
            doc_ref = self.db.collection('users').document(user_id)
            doc_ref.update({'profile': profile_data})
            
            logger.info(f"Perfil do usuário {user_id} atualizado")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao atualizar perfil: {e}")
            raise


# Instância global do serviço
firebase_service = FirebaseService() 