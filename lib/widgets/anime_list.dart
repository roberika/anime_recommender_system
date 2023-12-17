import 'package:flutter/material.dart';
import 'package:rkmdaa/screens/anime_detail_screen.dart';

import '../models/anime.dart';

class AnimeList extends StatefulWidget {
  const AnimeList({super.key, required this.animeList, required this.isHistory});
  final bool isHistory;
  final List<Anime> animeList;

  @override
  State<AnimeList> createState() => _AnimeListState();
}

class _AnimeListState extends State<AnimeList> {
  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: ListView.builder(
        itemBuilder: (context, index){
          return AnimeListItem(anime: widget.animeList[index], isHistory: widget.isHistory,);
        },
        itemCount: widget.animeList.length,
      ),
    );
  }
}

class AnimeListItem extends StatelessWidget {
  const AnimeListItem({super.key, required this.anime, required this.isHistory});
  final Anime anime;
  final bool isHistory;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: (){
        Navigator.push(context, MaterialPageRoute(builder: (context) => AnimeDetailScreen(anime: anime, isHistory: isHistory,)));
      },
      child: Row(
        children: [
          Expanded(
            child: Padding(
              padding: const EdgeInsets.symmetric(vertical: 2),
              child: Container(
                padding: EdgeInsets.all(4),
                decoration: BoxDecoration(border: Border.all(color: Colors.black)),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(anime.name),
                    Row(children: [
                      Text((anime.score ?? "—").toString()),
                      Expanded(child: Text(anime.id, textAlign: TextAlign.right,),),
                    ],)
                  ],
                ),
              ),
            ),
          )
        ],
      ),
    );
  }
}

