import '../anime_dictionary.dart';

class Anime {
  final String id;
  final String name;
  final double? score;

  Anime({
    required this.id,
    required this.name,
    this.score,
  });

  factory Anime.fromJson(Map<String, dynamic> json) {
    double score = double.parse(json["score"].toString());
    var anime = Anime(
      id: json["id"].toString(),
      name: json["name"].toString(),
      score: score == 0 ? null : score,
    );
    return anime;
  }
}

class AnimeDetail {
  final String id;
  final String name;
  final String animeURL;
  final double? predictedScore;
  final double? userScore;
  final double? malScore;
  final List<String> genres;
  final List<String> themes;
  final List<String> demographics;
  final List<String> producers;
  final List<String> licensors;
  final List<String> studios;
  final String? imageURL;
  final String? type;
  final String? source;
  final String? status;
  final String? aired;
  final int? rank;
  final String? season;
  final String? synopsis;
  final List<Map<String, List<LinkedItem>>> relations;

  AnimeDetail({
    required this.id,
    required this.name,
    required this.animeURL,
    this.predictedScore,
    this.userScore,
    this.malScore,
    this.genres = const [],
    this.themes = const [],
    this.demographics = const [],
    this.producers = const [],
    this.licensors = const [],
    this.studios = const [],
    this.relations = const [],
    this.imageURL,
    this.type,
    this.source,
    this.status,
    this.aired,
    this.rank,
    this.season,
    this.synopsis,
  });

  factory AnimeDetail.fromJson(
      Map<String, dynamic> json,
      double? predictedScore,
      double? userScore) {
    json = json["data"];
    List<String> genres = [for (var anime in json["genres"]) anime["name"]];
    List<String> themes = [for (var anime in json["themes"]) anime["name"]];
    List<String> demographics = [for (var anime in json["demographics"]) anime["name"]];
    List<String> producers =  [for (var anime in json["producers"]) anime["name"]];
    List<String> licensors = [for (var anime in json["licensors"]) anime["name"]];
    List<String> studios = [for (var anime in json["studios"]) anime["name"]];
    List<Map<String, List<LinkedItem>>> relations =   [for (var category in json["relations"]) {
      category["relation"] : [for (var anime in category["entry"])
        LinkedItem(name: anime["name"], url: anime["url"])]
    }];
    var anime = AnimeDetail(
      id: json["mal_id"].toString(),
      name: json["title"],
      animeURL: json["url"],
      predictedScore: predictedScore,
      userScore: userScore,
      malScore: json["score"],
      genres: genres,
      themes: themes,
      demographics: demographics,
      producers: producers,
      licensors: licensors,
      studios: studios,
      relations: relations,
      imageURL: json["images"]["jpg"]["image_url"],
      type: json["type"],
      source: json["source"],
      status: json["status"],
      aired: json["aired"]["string"],
      rank: json["rank"],
      season: json["season"],
      synopsis: json["synopsis"],
    );
    return anime;
  }
}

class LinkedItem {
  final String name;
  final String url;

  LinkedItem({
    required this.name,
    required this.url,
  });
}
