from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Movie
from .serializers import MovieSerializer
from .utils import get_all_movies, search_movies
from .permissions import IsAdmin, IsWorker

@api_view(['GET'])
@permission_classes([IsWorker])
def get_all_movies_api(request):
    movies = Movie.objects.filter(is_active=True)
    serialized_movies = MovieSerializer(movies, many=True).data

    tmdb_movies = get_all_movies()
    if isinstance(tmdb_movies, list):
        for movie_data in tmdb_movies:
            Movie.objects.get_or_create(
                title=movie_data['title'],
                defaults={
                    'description': movie_data.get('overview', ''),
                    'release_date': movie_data.get('release_date', ''),
                    'genre': movie_data.get('genre', 'Desconocido'),
                    'is_active': True,
                }
            )

        return Response(serialized_movies, status=status.HTTP_200_OK)
    else:
        return Response({"error": tmdb_movies}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsWorker])
def search_movies_api(request):
    query = request.query_params.get('query', '')
    if query:
        results = search_movies(query)
        return Response(results)
    else:
        return Response({"error": "Ingresar parámetro"}, status=400)


@api_view(['POST'])
@permission_classes([IsAdmin])
def create_movie(request):
    title = request.data.get('title')
    description = request.data.get('description')
    release_date = request.data.get('release_date')
    genre = request.data.get('genre')

    if not title or not description or not release_date or not genre:
        return Response({"error": "Todos los campos son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

    movie = Movie.objects.create(
        title=title,
        description=description,
        release_date=release_date,
        genre=genre
    )
    movie.save()
    return Response(MovieSerializer(movie).data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAdmin])
def update_movie(request, pk):
    try:
        movie = Movie.objects.get(pk=pk, is_active=True)
    except Movie.DoesNotExist:
        return Response({'error': 'Contenido no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    movie.title = request.data.get('title', movie.title)
    movie.description = request.data.get('description', movie.description)
    movie.release_date = request.data.get('release_date', movie.release_date)
    movie.genre = request.data.get('genre', movie.genre)
    movie.save()

    return Response(MovieSerializer(movie).data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAdmin])
def delete_movie(request, pk):
    try:
        movie = Movie.objects.get(pk=pk, is_active=True)
    except Movie.DoesNotExist:
        return Response({'error': 'Contenido no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    movie.is_active = False
    movie.save()

    return Response({'message': 'Contenido eliminado'}, status=status.HTTP_200_OK)
