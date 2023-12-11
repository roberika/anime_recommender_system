import 'package:animated_splash_screen/animated_splash_screen.dart';
import 'package:flutter/material.dart';
import 'package:rkmdaa/screens/profile_screen.dart';
import 'package:rkmdaa/screens/recommendation_screen.dart';
import 'package:rkmdaa/screens/search_screen.dart';

import 'models/user.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
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

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _currentIndex = 0;
  static User? user;

  final List<Widget> _children = [
    RecommendationScreen(),
    SearchScreen(),
    ProfileScreen(user: user),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _children[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index){
          setState(() {
            _currentIndex = index;
          });
        },
        items: [
          BottomNavigationBarItem(icon: Icon(Icons.recommend), label: "Recommendation"),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: "Search"),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: "Profile"),
        ],
      ),
    );
  }
}


