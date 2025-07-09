@echo off
echo 🚀 Iniciando serviços do PC-Estoque Bot...

REM Verificar se Docker está rodando
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker não está rodando. Por favor, inicie o Docker primeiro.
    pause
    exit /b 1
)

REM Iniciar PostgreSQL e Redis
echo 📦 Iniciando PostgreSQL e Redis...
docker-compose up -d

REM Aguardar os serviços ficarem prontos
echo ⏳ Aguardando serviços ficarem prontos...
timeout /t 10 /nobreak >nul

REM Verificar se os serviços estão rodando
docker ps | findstr "pc-postgres" >nul
if errorlevel 1 (
    echo ❌ Falha ao iniciar PostgreSQL
) else (
    echo ✅ PostgreSQL iniciado com sucesso
)

docker ps | findstr "redis" >nul
if errorlevel 1 (
    echo ❌ Falha ao iniciar Redis
) else (
    echo ✅ Redis iniciado com sucesso
)

echo.
echo 🤖 Agora você pode executar o bot:
echo python bot_simples.py
echo.
echo 📱 Use /start e depois /identificar seu_seller_id para começar
pause
