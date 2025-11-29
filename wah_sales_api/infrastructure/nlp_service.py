import os
import instructor
from openai import OpenAI
from dotenv import load_dotenv
from enum import Enum
from ..domain.models import PerfilInicial, PlanRecomendado, IntencionRespuesta, DatosAgendamiento, PerfilCompleto

class ModelProvider(str, Enum):
    OPENAI = "openai"
    DEEPSEEK = "deepseek"

class NLPService:
    def __init__(self):
        load_dotenv()
        # Load provider preference from environment variable, default to OpenAI
        self.provider = os.getenv("MODEL_PROVIDER", ModelProvider.OPENAI)

        # Initialize the appropriate client based on provider
        if self.provider == ModelProvider.DEEPSEEK:
            api_key = os.getenv("DEEPSEEK_API_KEY")
            base_url = "https://api.deepseek.com"
            model_name = "deepseek-chat"
        else:  # Default to OpenAI
            api_key = os.getenv("OPENAI_API_KEY")
            base_url = None  # OpenAI default
            model_name = "gpt-4o"

        if not api_key or api_key == "tu_clave_de_api_aqui":
            provider_name = "DEEPSEEK" if self.provider == ModelProvider.DEEPSEEK else "OPENAI"
            print(f"ADVERTENCIA: La clave {provider_name}_API_KEY no se ha configurado en el archivo .env. El servicio de NLP no funcionará.")
            self.client = None
            self.model_name = model_name
        else:
            # Initialize the client with the appropriate settings
            client_kwargs = {"api_key": api_key}
            if base_url:
                client_kwargs["base_url"] = base_url

            self.client = instructor.patch(OpenAI(**client_kwargs))
            self.model_name = model_name

    def _create_completion(self, response_model=None, **kwargs):
        """Helper method to create completions with the appropriate model"""
        kwargs["model"] = self.model_name
        if response_model:
            kwargs["response_model"] = response_model
        return self.client.chat.completions.create(**kwargs)

    def extract_initial_profile(self, message: str) -> PerfilInicial:
        return self._create_completion(
            response_model=PerfilInicial,
            messages=[
                {"role": "system", "content": "Extrae 'para quien son las clases' y la 'edad' de la respuesta del usuario."},
                {"role": "user", "content": message}
            ]
        )

    def recommend_plan(self, perfil: PerfilCompleto) -> PlanRecomendado:
        return self._create_completion(
            response_model=PlanRecomendado,
            messages=[
                {"role": "system", "content": "Eres un asistente de ventas. Con base en la motivación, objetivos y disponibilidad de tiempo del alumno, recomienda el plan 'basico', 'intermedio' o 'avanzado'. Usa 'basico' si el compromiso es bajo o el interés es exploratorio. Usa 'avanzado' si hay metas profesionales o alto compromiso."},
                {"role": "user", "content": f"Perfil del usuario: {perfil.model_dump_json()}"}
            ]
        )

    def generate_sales_pitch(self, perfil: PerfilCompleto, plan: dict) -> str:
        response = self._create_completion(
            messages=[
                {"role": "system", "content": "Actúa como un asesor de ventas cálido y profesional de una escuela de música. Conecta la historia del usuario con los beneficios del plan recomendado. Haz que se sienta comprendido, motivado y entusiasmado. Sé breve pero efectivo. Termina con una invitación clara y amigable para agendar una clase muestra gratuita."},
                {"role": "user", "content": f"Aquí tienes el perfil del usuario:\n{perfil.model_dump_json()}\n\nEl plan recomendado es: '{plan['nombre']}'. Sus detalles son:\n{plan['descripcion']}. Precio: ${plan['precio']}."}
            ]
        )
        return response.choices[0].message.content

    def classify_intent(self, message: str) -> IntencionRespuesta:
        return self._create_completion(
            response_model=IntencionRespuesta,
            messages=[
                {"role": "system", "content": "Clasifica la respuesta del usuario. 'afirmativa' si quiere agendar, 'negativa' si no quiere."},
                {"role": "user", "content": message}
            ]
        )

    def extract_scheduling_data(self, message: str) -> DatosAgendamiento:
        return self._create_completion(
            response_model=DatosAgendamiento,
            messages=[
                {"role": "system", "content": "Extrae el número de teléfono, día y hora de la respuesta del usuario para agendar una sesión. El número de teléfono es un campo requerido. El día y la hora son opcionales."},
                {"role": "user", "content": message}
            ]
        )

nlp_service = NLPService()
