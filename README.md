# Memer

Bot creador de memes para Discord

Hecho con [Discord.py](https://github.com/Rapptz/discord.py)

Actualmente se encuentra hosteado en Heroku.

[Link para añadir al bot](https://discord.com/api/oauth2/authorize?client_id=733072938273865749&permissions=8&scope=bot)

## Instalación

Si querés instalar el bot por tu cuenta, sos libre de hacerlo.
En el caso de que quieras usar Heroku, ya viene incluido el Procfile.
Notar que hay que crear un token en el
[Portal de Desarrolladores de Discord](https://discord.com/developers/applications)
para usarlo.

## Uso

Todos los mensajes enviados al bot deben comenzar por `;meme`.
Los parámetros del meme se separan con espacios. En el caso de que se quiera usar
más de una palabra en el argumento (como al momento de hacer un meme), se puede
indicar que es un solo argumento poniéndolo todo entre comillas dobles `""`

Ejemplo: `;meme drake "Memes con Paint" "Memes con Memer"` produce el siguiente meme:
![Ejemplo](https://cdn.discordapp.com/attachments/733103077107695677/738823867551973398/temp.jpg)

La lista completa de memes se puede obtener mediante el comando `;meme list`.
También se puede ver entrando a la carpeta `./img` en este repositorio.

## Lista de tareas

- [x] Poder añadirle texto a los memes
- [x] Poder añadir memes de forma arbitraria mediante JSON
- [x] Darle contraste al texto con un fondo blanco
- [x] Enviar los memes a un canal general definido
- [x] Eliminar el comando cuando el meme fue generado
- [x] Soporte de memes animados en forma de GIF
- [ ] Añadir una mayor cantidad de memes

## Contribuir

En el caso de que quieras añadir más memes, no hace falta crear una *branch*.
En el caso de cambios de mayor importancia, si es necesario.

## Licencia

Este proyecto se encuentra bajo la **MIT License**
