import 'package:flutter/material.dart';
import 'package:rkmdaa/anime_dictionary.dart';

import '../models/anime.dart';
import '../widgets/anime_list.dart';

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  TextEditingController searchController = TextEditingController();
  List<Anime> searchResults = [];

  void updateSearchResults () {
    setState(() {
      searchResults = AnimeDictionary.search(searchController.value.text);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: EdgeInsets.all(24),
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.only(top: 24.0),
              child: TextField(
                controller: searchController,
                decoration: InputDecoration(
                  prefixIcon: Icon(Icons.search),
                ),
                style: TextStyle(
                ),
                onEditingComplete: updateSearchResults,
              ),
            ),
            AnimeList(searchResults: searchResults,),
          ],
        ),
      ),
    );
  }
}
