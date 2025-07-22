"""
API Principal do Bebrew
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, List, Any
from loguru import logger
import uvicorn

from ..config.settings import get_settings, get_cors_origins
from ..services.ai_service import ai_service
from ..services.firebase_service import firebase_service


# Configurações
settings = get_settings()

# Inicialização do FastAPI
app = FastAPI(
    title="Bebrew API",
    description="API do sistema de controle de produção para brassagem artesanal",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Autenticação
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Obtém usuário atual baseado no token"""
    try:
        token = credentials.credentials
        user_data = await firebase_service.verify_token(token)
        return user_data
    except Exception as e:
        logger.error(f"Erro na autenticação: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado"
        )


# Rotas de Saúde
@app.get("/")
async def root():
    """Rota raiz"""
    return {
        "message": "Bebrew API - Sistema de Controle de Produção para Brassagem",
        "version": "1.0.0",
        "status": "online"
    }


@app.get("/health")
async def health_check():
    """Verificação de saúde da API"""
    return {
        "status": "healthy",
        "services": {
            "firebase": "connected",
            "openai": "ready"
        }
    }


# Rotas de Autenticação
@app.post("/auth/register")
async def register_user(email: str, password: str, display_name: str = None):
    """Registra um novo usuário"""
    try:
        user_data = await firebase_service.create_user(email, password, display_name)
        return {
            "message": "Usuário criado com sucesso",
            "user": user_data
        }
    except Exception as e:
        logger.error(f"Erro ao registrar usuário: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post("/auth/verify")
async def verify_token(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Verifica token de autenticação"""
    return {
        "message": "Token válido",
        "user": current_user
    }


# Rotas de Receitas
@app.post("/recipes")
async def create_recipe(
    recipe_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Cria uma nova receita"""
    try:
        recipe_id = await firebase_service.save_recipe(current_user["uid"], recipe_data)
        return {
            "message": "Receita criada com sucesso",
            "recipe_id": recipe_id
        }
    except Exception as e:
        logger.error(f"Erro ao criar receita: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar receita"
        )


@app.get("/recipes")
async def get_recipes(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Obtém todas as receitas do usuário"""
    try:
        recipes = await firebase_service.get_user_recipes(current_user["uid"])
        return {
            "recipes": recipes,
            "count": len(recipes)
        }
    except Exception as e:
        logger.error(f"Erro ao obter receitas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter receitas"
        )


@app.get("/recipes/{recipe_id}")
async def get_recipe(
    recipe_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Obtém uma receita específica"""
    try:
        recipe = await firebase_service.get_recipe(current_user["uid"], recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receita não encontrada"
            )
        return {"recipe": recipe}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao obter receita: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter receita"
        )


@app.put("/recipes/{recipe_id}")
async def update_recipe(
    recipe_id: str,
    recipe_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Atualiza uma receita"""
    try:
        success = await firebase_service.update_recipe(
            current_user["uid"], recipe_id, recipe_data
        )
        if success:
            return {"message": "Receita atualizada com sucesso"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receita não encontrada"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao atualizar receita: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar receita"
        )


@app.delete("/recipes/{recipe_id}")
async def delete_recipe(
    recipe_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Deleta uma receita"""
    try:
        success = await firebase_service.delete_recipe(current_user["uid"], recipe_id)
        if success:
            return {"message": "Receita deletada com sucesso"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Receita não encontrada"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro ao deletar receita: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao deletar receita"
        )


# Rotas de IA
@app.post("/ai/analyze-recipe")
async def analyze_recipe(
    recipe_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Analisa uma receita usando IA"""
    try:
        analysis = await ai_service.analyze_recipe(recipe_data)
        return {"analysis": analysis}
    except Exception as e:
        logger.error(f"Erro ao analisar receita: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao analisar receita"
        )


@app.post("/ai/optimize-recipe")
async def optimize_recipe(
    recipe_data: Dict[str, Any],
    target_style: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Otimiza uma receita para um estilo específico"""
    try:
        optimization = await ai_service.optimize_recipe(recipe_data, target_style)
        return {"optimization": optimization}
    except Exception as e:
        logger.error(f"Erro ao otimizar receita: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao otimizar receita"
        )


@app.post("/ai/predict-fermentation")
async def predict_fermentation(
    recipe_data: Dict[str, Any],
    initial_gravity: float,
    temperature: float,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Prediz comportamento da fermentação"""
    try:
        prediction = await ai_service.predict_fermentation(
            recipe_data, initial_gravity, temperature
        )
        return {"prediction": prediction}
    except Exception as e:
        logger.error(f"Erro ao prever fermentação: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao prever fermentação"
        )


@app.post("/ai/suggest-improvements")
async def suggest_improvements(
    production_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Sugere melhorias baseadas em dados de produção"""
    try:
        suggestions = await ai_service.suggest_improvements(production_data)
        return {"suggestions": suggestions}
    except Exception as e:
        logger.error(f"Erro ao gerar sugestões: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao gerar sugestões"
        )


# Rotas de Produção
@app.post("/productions")
async def create_production(
    production_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Cria uma nova produção"""
    try:
        production_id = await firebase_service.save_production(
            current_user["uid"], production_data
        )
        return {
            "message": "Produção criada com sucesso",
            "production_id": production_id
        }
    except Exception as e:
        logger.error(f"Erro ao criar produção: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar produção"
        )


@app.get("/productions")
async def get_productions(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Obtém todas as produções do usuário"""
    try:
        productions = await firebase_service.get_user_productions(current_user["uid"])
        return {
            "productions": productions,
            "count": len(productions)
        }
    except Exception as e:
        logger.error(f"Erro ao obter produções: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter produções"
        )


# Rotas de Ingredientes
@app.post("/ingredients")
async def create_ingredient(
    ingredient_data: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Cria um novo ingrediente no inventário"""
    try:
        ingredient_id = await firebase_service.save_ingredient(
            current_user["uid"], ingredient_data
        )
        return {
            "message": "Ingrediente adicionado com sucesso",
            "ingredient_id": ingredient_id
        }
    except Exception as e:
        logger.error(f"Erro ao adicionar ingrediente: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao adicionar ingrediente"
        )


@app.get("/ingredients")
async def get_ingredients(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Obtém todos os ingredientes do usuário"""
    try:
        ingredients = await firebase_service.get_user_ingredients(current_user["uid"])
        return {
            "ingredients": ingredients,
            "count": len(ingredients)
        }
    except Exception as e:
        logger.error(f"Erro ao obter ingredientes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter ingredientes"
        )


# Configuração de logging
logger.add(
    "logs/bebrew_api.log",
    rotation="1 day",
    retention="30 days",
    level=settings.log_level
)


if __name__ == "__main__":
    uvicorn.run(
        "backend.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    ) 