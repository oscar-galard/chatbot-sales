# URL de la API del bot
API_URL="http://localhost:8000/api/v1/lead" # Nuevo endpoint para el microservicio

# Generar un ID de sesión único para esta conversación
# Esto simula cómo un frontend mantendría un ID de sesión para un usuario.
SESSION_ID=$(uuidgen)

# Variable para almacenar la fase actual de la conversación (manejada por el servidor)
current_phase=""

echo "🚀 Bot de Ventas Interactivo"
echo "------------------------------------------------------------------"

# --- Primera Interacción: Iniciar la Conversación ---
# Enviamos un mensaje vacío con el nuevo SESSION_ID.
# La API de FastAPI detectará que es una nueva sesión y enviará el saludo inicial
# y la primera pregunta de la fase 'ask_connect_1'.
echo "Iniciando nueva conversación con ID de sesión: $SESSION_ID"
response=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"\"}" "$API_URL")

# --- Manejo de Errores al Inicio ---
# Verifica si la respuesta contiene un error HTTP (campo 'detail')
if echo "$response" | jq -e '.detail' > /dev/null; then
    error_detail=$(echo "$response" | jq -r '.detail')
    echo "❌ Error al iniciar la API: $error_detail"
    echo "Asegúrate de que el microservicio de FastAPI esté corriendo en http://localhost:8000 y sea accesible."
    exit 1 # Sale del script si hay un error crítico al inicio
fi

# Extraer la respuesta del bot y la fase inicial
bot_response=$(echo "$response" | jq -r '.response')
current_phase=$(echo "$response" | jq -r '.phase')
# data_output=$(echo "$response" | jq -r '.data') # Opcional: capturar datos iniciales si los hubiera

echo "🤖 >> $bot_response"
echo "------------------------------------------------------------------"

# --- Bucle Principal de la Conversación ---
# La conversación continúa mientras la fase no sea "closed" (cerrada)
while [[ "$current_phase" != "closed" ]]; do
    # Muestra la fase actual para el usuario
    read -p "👤 ($current_phase) >> " user_message
    
    # Enviar la petición a la API de FastAPI con el mensaje del usuario y el SESSION_ID
    response=$(curl -s -X POST -H "Content-Type: application/json" -d "{\"session_id\": \"$SESSION_ID\", \"message\": \"$user_message\"}" "$API_URL")

    # --- Manejo de Errores en el Bucle ---
    # Verifica si la respuesta contiene un error HTTP
    if echo "$response" | jq -e '.detail' > /dev/null; then
        error_detail=$(echo "$response" | jq -r '.detail')
        echo "❌ Error de la API: $error_detail"
        echo "La conversación podría haberse roto o reiniciado. Por favor, intenta iniciar una nueva."
        current_phase="closed" # Forzar la salida del bucle
        continue # Salta al siguiente ciclo del bucle (que ahora terminará)
    fi

    # Extraer la respuesta del bot y la nueva fase
    bot_response=$(echo "$response" | jq -r '.response')
    current_phase=$(echo "$response" | jq -r '.phase')
    data_output=$(echo "$response" | jq -r '.data') # Capturar el objeto 'data'

    # Imprimir la respuesta del bot
    echo "🤖 >> $bot_response"

    # --- Mostrar Datos de Agendamiento (si existen y la conversación se cerró) ---
    # Si la fase es 'closed' y el objeto 'data' contiene la clave 'agendamiento',
    # significa que se agendó una cita y se extrajeron los datos.
    if [[ "$current_phase" == "closed" ]] && [[ $(echo "$data_output" | jq 'has("agendamiento")') == "true" ]]; then
        echo "📝 Datos de agendamiento extraídos:"
        echo "$data_output" | jq '.agendamiento' # Imprime el objeto JSON de agendamiento
    fi

    echo "------------------------------------------------------------------"
done

echo "✅ Conversación finalizada. ¡Gracias por usar el bot!"
