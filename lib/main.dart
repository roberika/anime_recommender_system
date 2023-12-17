import 'dart:convert';

import 'package:animated_splash_screen/animated_splash_screen.dart';
import 'package:flutter/material.dart';
import 'package:rkmdaa/screens/profile_screen.dart';
import 'package:rkmdaa/screens/anime_list_screen.dart';
import 'package:rkmdaa/screens/search_screen.dart';
import 'package:http/http.dart' as http;

import 'anime_dictionary.dart';
import 'models/anime.dart';
import 'models/user.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
            seedColor: Colors.blueGrey,
        ),
        useMaterial3: true,

      ),
      home: AnimatedSplashScreen(
          splash: Container(
            //decoration: BoxDecoration(border: Border.all(color: Colors.amber)),
            padding: EdgeInsets.all(32.0),
            child: Image.asset("images/logo.png"),
          ),
          duration: 3000,
          splashIconSize: double.infinity,
          splashTransition: SplashTransition.fadeTransition,
          backgroundColor: Colors.blue,
          nextScreen: MainScreen()),
    );
  }
}

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  static User? user;
  static List<Anime> history = [];
  static List<Anime> recommendations = [];

  static Future<User?> retrieveUser(String username) async {
    final response = await http.get(
      Uri.parse(
          'https://api.jikan.moe/v4/users/' + username),
    );
    if (response.statusCode == 200) {
      user = User.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
      retrieveRecommendations(username);
      retrieveHistory(username);
      return user;
    } else {
      throw Exception('Failed to retrive user.');
    }
  }

  static void retrieveHistory(String username) async {
    final response = await http.get(
        Uri.parse("https://rkmdaa-py-server.vercel.app/history/" + username)
    );
    if (response.statusCode == 200) {
      Map<String, dynamic> json = jsonDecode(response.body) as Map<String, dynamic>;
      history = [for (var anime in json["data"]) Anime.fromJson(anime)];
    } else {
      throw Exception('Failed to retrieve user history.');
    }
  }

  static void retrieveRecommendations(String username) async {
    final response = await http.get(
      Uri.parse('https://rkmdaa-py-server.vercel.app/recommend/' + username),
    );
    if (response.statusCode == 200) {
      Map<String, dynamic> json = jsonDecode(response.body) as Map<String, dynamic>;
      recommendations = [for (var anime in json["data"]) Anime.fromJson(anime)];
    } else {
      throw Exception('Failed to retrieve user recommendations.');
    }
  }

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _currentIndex = 0;

  @override
  Widget build(BuildContext context) {
    final recommendations = MainScreen.recommendations;
    final history = MainScreen.history;
    User? user = MainScreen.user;
    final List<Widget> children = [
      SearchScreen(),
      AnimeListScreen(
        animeList: recommendations,
        title: 'Recommendations',
        emptyListLabel: 'We can\'t recommend you anything as you\'ve not inputted your username',
        isHistory: false,
      ),
      AnimeListScreen(
        animeList: history,
        title: 'History',
        emptyListLabel: 'We can\'t show your history as you\'ve not inputted your username',
        isHistory: true,
      ),
      ProfileScreen(),
    ];
    return Scaffold(
      body: children[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        selectedItemColor: Colors.blue,
        unselectedItemColor: Colors.blueGrey,
        enableFeedback: false,
        backgroundColor: Colors.white,
        selectedFontSize: 11.0,
        unselectedFontSize: 11.0,
        currentIndex: _currentIndex,
        onTap: (index){
          setState(() {
            _currentIndex = index;
          });
        },
        items: [
          BottomNavigationBarItem(icon: Icon(Icons.search), label: "Search"),
          BottomNavigationBarItem(icon: Icon(Icons.recommend), label: "Recommendation"),
          BottomNavigationBarItem(icon: Icon(Icons.history), label: "History"),
          user == null
              ? BottomNavigationBarItem(icon: Icon(Icons.person_outlined), label: "Profile")
              : BottomNavigationBarItem(icon: Icon(Icons.person), label: user!.username),
        ],
      ),
    );
  }
}


