# Chaos

Les fichiers qui ont servi à générer les animations et figures de ma vidéo sur le chaos
https://www.youtube.com/watch?v=YrOyRCD7M14

Ils sont là uniquement pour info, pour ceux qui connaissent déjà Python. Je n'ai malheureusement pas le temps d'assurer le service après vente :-)

A savoir :
* Tous les fichiers sont indépendants les uns des autres, et sont plus ou moins numérotés dans l'ordre où ils apparaissent dans la vidéo
* Il faut avoir les packages scientifiques "classiques" : numpy, scipy, matplotlib...je recommande les distributions qui contiennent déjà tout ce qu'il faut comme Anaconda ou Winpython
* Pour générer les films, il faut avoir installé ffmpeg quelque part sur votre disque, et renseigné son chemin dans chaque fichier, au niveau de la ligne :

plt.rcParams['animation.ffmpeg_path'] = r'/Volumes/Data/Youtube/[ffmpeg]/ffmpeg'

Bonne chance :-)

David
