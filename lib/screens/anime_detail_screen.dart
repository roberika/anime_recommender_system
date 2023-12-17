import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:rkmdaa/main.dart';
import 'package:rkmdaa/widgets/anime_list.dart';

import '../models/anime.dart';
import 'package:http/http.dart' as http;

import '../models/user.dart';

class AnimeDetailScreen extends StatefulWidget {
  AnimeDetailScreen(
      {super.key, required Anime anime, required bool isHistory}) {
    animeDetail = AnimeDetail(
      id: anime.id,
      name: anime.name,
      animeURL: "https://myanimelist.net/",
      predictedScore: isHistory ? null : anime.score,
      userScore: isHistory ? anime.score : null,
    );
  }
  late AnimeDetail animeDetail;

  @override
  State<AnimeDetailScreen> createState() => _AnimeDetailScreenState();
}

class _AnimeDetailScreenState extends State<AnimeDetailScreen> {
  bool showFullDetail = false;
  late AnimeDetail animeDetail;
  List<Anime> recommendations = [];
  User? user = MainScreen.user;

  void retrieveAnime() async {
    animeDetail = widget.animeDetail;
    final response = await http.get(
      Uri.parse('https://api.jikan.moe/v4/anime/' +
          widget.animeDetail.id.toString() +
          "/full"),
    );
    if (response.statusCode == 200) {
      setState(() {
        animeDetail = AnimeDetail.fromJson(
            jsonDecode(response.body) as Map<String, dynamic>,
            widget.animeDetail.predictedScore,
            widget.animeDetail.userScore);
      });
    } else {
      throw Exception('Failed to retrive anime detail.');
    }
  }

  void retrieveRecommendations() async {
    final response = await http.get(
      user == null
          ? Uri.parse('https://rkmdaa-py-server.vercel.app/recommend/0/' +
              widget.animeDetail.id.toString())
          : Uri.parse('https://rkmdaa-py-server.vercel.app/recommend/' +
              user!.username +
              '/' +
              widget.animeDetail.id.toString()),
    );
    if (response.statusCode == 200) {
      Map<String, dynamic> json =
          jsonDecode(response.body) as Map<String, dynamic>;
      setState(() {
        recommendations = [
          for (var anime in json["data"]) Anime.fromJson(anime)
        ];
      });
    } else {
      throw Exception('Failed to retrieve user recommendations.');
    }
  }

  @override
  void initState() {
    super.initState();
    retrieveAnime();
    retrieveRecommendations();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        fit: StackFit.loose,
        alignment: AlignmentDirectional.bottomEnd,
        children: [
          Padding(
            padding: const EdgeInsets.all(12.0),
            child: Column(
              children: [
                Row(
                  children: [
                    Container(
                      decoration: BoxDecoration(
                          border: Border.all(color: Colors.black),
                          borderRadius: BorderRadius.circular(5),
                          shape: BoxShape.rectangle),
                      child: animeDetail.imageURL == null
                          ? Image.asset(
                              "images/logo.png",
                              // Ratio 16 x 9
                              width: MediaQuery.of(context).size.width / 3,
                              height:
                                  MediaQuery.of(context).size.width / 2,
                              fit: BoxFit.fitWidth,
                            )
                          : Image.network(
                              animeDetail.imageURL!,
                              // Ratio 16 x 9
                              width: MediaQuery.of(context).size.width / 3,
                              height:
                                  MediaQuery.of(context).size.width / 2,
                              fit: BoxFit.fitWidth,
                            ),
                    ),
                    Expanded(
                        child: Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: Column(
                        children: [
                          Text(
                            animeDetail.name,
                            maxLines: 5,
                            overflow: TextOverflow.ellipsis,
                            style: TextStyle(fontSize: 18, height: 1.2),
                          ),
                          SizedBox(
                            height: 8,
                          ),
                          Text(
                            RegExp(r'(?<=\[)(.*)(?=\])')
                                .firstMatch((animeDetail.genres +
                                        animeDetail.themes +
                                        animeDetail.demographics)
                                    .toString())!
                                .group(0)!,
                            maxLines: 3,
                            overflow: TextOverflow.ellipsis,
                            style: TextStyle(fontSize: 14, height: 1.2),
                          ),
                          SizedBox(
                            height: 8,
                          ),
                          Text(
                              animeDetail.season == null
                                  ? (animeDetail.aired ?? "")
                                  : animeDetail.season!.capitalize() +
                                      (" - " + (animeDetail.aired ?? "")),
                              style: TextStyle(fontSize: 12, height: 1.2)),
                        ],
                      ),
                    )),
                  ],
                ),
                SizedBox(
                  height: 16,
                ),
                GestureDetector(
                  onTap: () {
                    setState(() {
                      showFullDetail = !showFullDetail;
                    });
                  },
                  child: Container(
                    decoration: BoxDecoration(
                        border: Border.all(color: Colors.white)),
                    child: showFullDetail
                        ? FullDetails(details: animeDetail.synopsis ?? "")
                        : FadeDetails(details: animeDetail.synopsis ?? ""),
                  ),
                ),
                AnimeList(animeList: recommendations, isHistory: animeDetail.userScore != null)
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.only(bottom: 48),
            child: Container(
              width: 35,
              child: Column(mainAxisAlignment: MainAxisAlignment.end,children: [
                if (animeDetail.userScore != null) Score(
                  score: animeDetail.userScore!,
                  color: Colors.green,
                ),
                if (animeDetail.predictedScore != null) Score(
                    score: animeDetail.predictedScore!,
                  color: Colors.yellow.shade800,
                ),
                if (animeDetail.malScore != null) Score(
                  score: animeDetail.malScore!,
                  color: Colors.blue,
                ),
              ],),
            ),
          ),
        ],
      ),
    );
  }
}
class Score extends StatelessWidget {
  Score({super.key, required this.score, required this.color});
  double score;
  Color color;

  @override
  Widget build(BuildContext context) {
    return  Column(
      children: [
        Container(
          color: color,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              Padding(
                padding: const EdgeInsets.all(2.0),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Text(
                      score.floor().toString(),
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    Text(
                      (score % 1).toStringAsFixed(2).substring(1),
                      style: TextStyle(
                        fontSize: 8,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
        SizedBox(height: 2,)
      ],
    );
  }
}


class FullDetails extends StatelessWidget {
  FullDetails({super.key, required this.details});
  String details;

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        Flexible(
          child: Text(
            details,
            style: TextStyle(fontSize: 12, height: 1.2),
          ),
        ),
      ],
    );
  }
}

class FadeDetails extends StatelessWidget {
  FadeDetails({super.key, required this.details});
  String details;

  @override
  Widget build(BuildContext context) {
    return Stack(
      alignment: AlignmentDirectional.bottomCenter,
      children: [
        Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              foregroundDecoration: BoxDecoration(
                  color: Colors.black,
                  gradient: LinearGradient(colors: [
                    Colors.white.withOpacity(0),
                    Colors.white,
                  ], begin: Alignment.topCenter, end: Alignment.bottomCenter)),
              height: MediaQuery.of(context).size.height / 13,
              child: Text(
                details,
                style: TextStyle(fontSize: 12, height: 1.2),
              ),
            ),
            Icon(Icons.arrow_drop_down)
          ],
        ),
      ],
    );
  }
}

extension StringExtension on String {
  String capitalize() {
    return "${this[0].toUpperCase()}${this.substring(1).toLowerCase()}";
  }
}