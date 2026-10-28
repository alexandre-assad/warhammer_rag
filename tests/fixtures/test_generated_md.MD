# Guide d'utilisation de Nébuleuse

Bienvenue dans le guide de Nébuleuse. Ce document sert de jeu d'essai pour le découpage en chunks. Il a été généré par l'IA.

## Installation

Pour installer l'application, exécutez la commande d'installation puis redémarrez le terminal.

## Configuration

La configuration se fait dans    separators = ['\n\n','\n','. ', '? ', '! ', '; '] un fichier unique situé à la racine du projet. Elle permet de régler la langue, le fuseau horaire et le niveau de journalisation. Chaque paramètre possède une valeur par défaut raisonnable, ce qui permet de démarrer sans rien modifier.

Les paramètres avancés concernent le cache et la connexion à la base de données. Il est recommandé de les modifier uniquement si vous rencontrez des problèmes de performance, car une mauvaise valeur peut ralentir fortement l'application.

Enfin, les variables d'environnement ont priorité sur le fichier de configuration. Cela permet d'adapter le comportement de l'application selon l'environnement, par exemple en développement, en test ou en production. Pensez à documenter chaque variable utilisée par votre équipe.

## Utilisation

Cette section est volontairement écrite sur une seule ligne, sans saut de ligne ni paragraphe. Le découpage doit donc se faire sur les fins de phrase. L'application démarre avec la commande principale. Elle affiche ensuite un tableau de bord synthétique. Chaque widget peut être déplacé à la souris. Les préférences sont enregistrées automatiquement à la fermeture. Est-ce que tout fonctionne hors ligne ? Oui, sauf la synchronisation ! Les données sont alors mises en file d'attente; elles partent dès le retour du réseau. Un journal détaillé reste consultable à tout moment dans le menu d'aide. Pour finir, pensez à vérifier régulièrement les mises à jour disponibles.

## Annexes

## Exemples

Voici un exemple de commande :

```bash
# lancer l'application
nebuleuse --langue fr --verbeux
```

| Option      | Description              |
|-------------|--------------------------|
| --langue    | Langue de l'interface    |
| --verbeux   | Active les logs détaillés |

Liste des raccourcis :

- Ctrl+S : sauvegarder
- Ctrl+Q : quitter
- Ctrl+Z : annuler

### Détails

Ce sous-titre de niveau 3 sert à vérifier que le découpage sur `##` ne le déforme pas.