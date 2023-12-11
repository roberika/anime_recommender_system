import 'package:flutter/material.dart';
import 'package:rkmdaa/screens/anime_detail_screen.dart';

import '../models/anime.dart';

class AnimeList extends StatefulWidget {
  const AnimeList({super.key, required this.searchResults});
  final List<Anime> searchResults;

  @override
  State<AnimeList> createState() => _AnimeListState();
}

class _AnimeListState extends State<AnimeList> {
  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: ListView.builder(
        itemBuilder: (context, index){
          return AnimeListItem(anime: widget.searchResults[index]);
        },
        itemCount: widget.searchResults.length,
      ),
    );
  }
}

class AnimeListItem extends StatelessWidget {
  const AnimeListItem({super.key, required this.anime});
  final Anime anime;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: (){
        Navigator.push(context, MaterialPageRoute(builder: (context) => AnimeDetailScreen()));
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
                    Text(anime.id),
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

