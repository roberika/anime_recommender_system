import 'package:flutter/material.dart';

import '../main.dart';
import '../models/anime.dart';
import '../models/user.dart';
import '../widgets/anime_list.dart';

class AnimeListScreen extends StatefulWidget {
  AnimeListScreen(
      {super.key,
      required this.animeList,
      required this.title,
      required this.emptyListLabel,
      required this.isHistory});
  List<Anime> animeList;
  String title;
  String emptyListLabel;
  bool isHistory;

  @override
  State<AnimeListScreen> createState() => _AnimeListScreenState();
}

class _AnimeListScreenState extends State<AnimeListScreen> {
  int sortMode = 0;
  late List<Anime> listAnime;
  void changeSort() {
    sortMode = (sortMode + 1) % 5;
    setState(() {
      switch (sortMode) {
        case 0:
          listAnime.sort((a, b) {
            double x = a.score ?? 0;
            double y = b.score ?? 0;
            return x.compareTo(y);
          });
          break;
        case 1:
          listAnime.sort((a, b) {
            double x = a.score ?? 0;
            double y = b.score ?? 0;
            return y.compareTo(x);
          });
          break;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    setState(() {
      listAnime = widget.animeList;
    });
    return Scaffold(
      body: Padding(
        padding: EdgeInsets.all(24),
        child: Column(
          children: [
            Row(
              children: [
                Expanded(child: Text(widget.title)),
                IconButton(onPressed: changeSort, icon: const Icon(Icons.sort))
              ],
            ),
            listAnime.isEmpty
                ? Expanded(child: Text(widget.emptyListLabel))
                : AnimeList(animeList: listAnime, isHistory: widget.isHistory),
          ],
        ),
      ),
    );
  }
}
