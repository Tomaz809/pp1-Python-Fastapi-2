from fastapi import FastAPI, Body, Query, Path

app = FastAPI()

app.title = "Cartelera"

@app.get("/")
def home():
    return {"message": "Welcome to the Cuevana!"}

peliculas = [
    {"id": 1, "titulo": "Bend It Like Beckham", "categoria": "comedia", "productor": "Kihn, Reichert and Heidenreich", "calidad": 4, "horario": "18:00", "activo": True},
    {"id": 2, "titulo": "Red Riding: 1983", "categoria": "drama", "productor": "Hansen-Okuneva", "calidad": 3, "horario": "20:30", "activo": True},
    {"id": 3, "titulo": "School of Rock", "categoria": "musical", "productor": "Hintz, Mraz and Bins", "calidad": 5, "horario": "22:00", "activo": False},
    {"id": 4, "titulo": "The Great Northfield Minnesota Raid", "categoria": "western", "productor": "Paucek-Luettgen", "calidad": 2, "horario": "17:15", "activo": False},
    {"id": 5, "titulo": "Bandaged", "categoria": "suspenso", "productor": "O'Connell Inc", "calidad": 3, "horario": "19:45", "activo": True},
    {"id": 6, "titulo": "Away from Her", "categoria": "romance", "productor": "Konopelski Group", "calidad": 4, "horario": "21:00", "activo": False},
    {"id": 7, "titulo": "Foreign Letters", "categoria": "drama", "productor": "Bernier-Connelly", "calidad": 2, "horario": "16:30", "activo": False},
    {"id": 8, "titulo": "American Astronaut, The", "categoria": "ciencia ficción", "productor": "Crooks-Skiles", "calidad": 5, "horario": "23:15", "activo": False},
    {"id": 9, "titulo": "Billu", "categoria": "comedia", "productor": "Connelly-Powlowski", "calidad": 3, "horario": "19:00", "activo": True},
    {"id": 10, "titulo": "Once Upon a Honeymoon", "categoria": "romance", "productor": "Hahn, Sporer and Bernier", "calidad": 4, "horario": "20:00", "activo": False}
]

#1. get para ver la cartelera completa.
@app.get("/cartelera")
async def movies():
    return peliculas

#2. get por id para buscar usando path
@app.get("/movie/{id}")
async def buscarPelicula(
    id: int = Path(gt=0, description="El ID tiene que ser mayor a 0(cero)")
):
    for movie in peliculas:
        if movie["id"] == id:
            return movie
    return {"detail": "Pelicula no encontrada"}

#3. post para agregar una pelicula nueva
@app.post("/Movie-nueva")
async def nuevaPelicula(
    id: int = Body(gt=0),
    titulo: str = Body(min_length=2, max_length=50),
    categoria: str = Body(min_length=2, max_length=50),
    productor: str = Body(min_length=2, max_length=50),
    calidad: float = Body(ge=0),
    horario: str = Body(min_length=2, max_length=5),
):
    nueva_pelicula = {
        "id": id,
        "titulo": titulo,
        "categoria": categoria,
        "productor": productor,
        "calidad":  calidad,
        "horario": horario,
        "activo": True
    }
    peliculas.append(nueva_pelicula)
    return nueva_pelicula

#4. put para editar datos de las peliculas usando path para buscar y body para modificar los datos.
@app.put("/modificar-peliculas/{id}")
async def editar_pelicula(
    id: int = Path(gt=0, description="ID de la pelicula a editar"),
    titulo: str = Body(min_length=2, max_length=50),
    categoria: str = Body(min_length=2, max_length=50),
    productor: str = Body(min_length=2, max_length=50),
    calidad: float = Body(ge=0),
    horario: str = Body(min_length=2, max_length=5),
):
    for m in peliculas:
        if m["id"] == id:            
            m["titulo"] = titulo
            m["categoria"] = categoria
            m["productor"] = productor
            m["calidad"] = calidad
            m["horario"] = horario
            return m
    return {"detail": "Artista no encontrado"}

#5. delete para borrado logico y fisico usando query para elegir el tipo.
@app.delete("/movie/{id}")
async def borrar_pelicula(
    id: int = Path(gt=0),
    logico: bool = Query(default=False, description="¿Quiere desactivar la pelicula?")
):
    for a in peliculas:
        if a["id"] == id:
            if logico:
                a["activo"] = False
                return {"detail": "Desactivando de la lista"}
            else:
                peliculas.remove(a)
                return {"detail": "Eliminando de la lista"}
    return {"detail": "Pelicula no encontrada"}


