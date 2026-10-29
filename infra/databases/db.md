Pour gérer notre Database, nous avons un fichier .sqlite qui nous force à utiliser SQLite. J'aurais préférer POSTGRESql notamment pour les meilleures pratiques qui l'accompagnent mais on a pas le choix.
Il fallait donc réaliser un read-only de la DB ainsi qu'une fonction qui execute une query.
On ne peut pas vraiment faire plus (thread, fonctions spécialisés par query) du à la techno et le nombre important de tables.
On a donc une fonction avec un fetchmany pour la mémoire et le contexte plus tard, en read only, avec des try catch en cas d'erreur.