from ai_engineer_01_amisr14_ai.integrations.openai_client import (create_openai_client, get_model_name)

def main()-> None:
    client=    create_openai_client()
    model= get_model_name()
    response= client.responses.create(
        model = model,
        input=( 
            "Responde en español en una sola frase: "
            "¿Cuál es el objetivo de un informe técnico semanal?"
        ),
    )
    print("Modelo Utilizado:", model)
    print("Respuesta del Modelo:", response.output_text)

if __name__ == "__main__":
    main()
