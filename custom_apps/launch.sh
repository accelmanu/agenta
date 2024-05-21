#!/bin/bash

echo "How do you want to initialize your app?"
options=("Single Prompt Application" "Chat Application")
select opt in "${options[@]}"; do
    case $opt in
        "Single Prompt Application")
            echo "Initializing Single Prompt Application"
            cd single_prompt_app
            break;;
        "Chat Application")
            echo "Initializing Chat Application"
            cd chat_app
            break;;
        *) echo "Invalid option";;
    esac
done

echo "Please enter the app name: "
read APP_NAME
if [ -z "$APP_NAME" ]; then
    echo "Error: App name not provided."
    exit 1
fi

echo "Please enter OpenAI endpoint: "
read API_BASE
if [ -z "$API_BASE" ]; then
    echo "Error: OpenAI endpoint not provided."
    exit 1
fi

echo "Please enter OpenAI access key: "
read -s API_KEY
if [ -z "$API_KEY" ]; then
    echo "Error: OpenAI access key not provided."
    exit 1
fi

echo "OPENAI_API_BASE=$API_BASE" > .env
echo "OPENAI_API_KEY=$API_KEY" >> .env

agenta init --app_name $APP_NAME --backend-host http://localhost

echo
echo "Be Patient! Your app \033[0;32m$APP_NAME\033[0m is getting deployed..."

agenta variant serve --file_name app.py