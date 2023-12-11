import 'package:animated_splash_screen/animated_splash_screen.dart';
import 'package:flutter/material.dart';

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
  @override
  Widget build(BuildContext context) {
    return const Placeholder();
  }
}


