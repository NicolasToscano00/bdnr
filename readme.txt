creo entorno virtual:
python -m venv venv
venv\Scripts\activate

en mac:
python3 -m venv venv
source venv/bin/activate

instalo 
pip install -r requirements.txt
hay algunos imports que pueden llegar a seguir dando error, no quiere decir que no funcione, probar igual.


ejecutar para tener corriendo redis en docker
docker run -d -p 6379:6379 redis:7

para ejecutar uso este comando
uvicorn app.main:app --reload