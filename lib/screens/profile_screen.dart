import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:rkmdaa/widgets/profile_image.dart';
import 'package:rkmdaa/widgets/profile_info_item.dart';
import 'package:http/http.dart' as http;

import '../models/user.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final TextEditingController usernameController = TextEditingController();
  User? user;
  String? username;

  void retrieveUser() async {
    final response = await http.get(
      Uri.parse(
          'https://api.jikan.moe/v4/users/' + usernameController.value.text),
    );
    if (response.statusCode == 200) {
      setState(() {
        user = User.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
      });
    } else {
      throw Exception('Failed to retrive user.');
    }
    build(context);
  }

  User getUser() {
    if (user == null) {
      return User(
        id: "-",
        username: "-",
        imageURL: null,
        linkURL: "https://myanimelist.net/panel.php",
        lastOnline: "-",
        gender: "-",
        birthday: "-",
        location: "-",
        joined: "-",
      );
    } else {
      return user!;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: Padding(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        children: [
          ProfileImage(
            imageURL: getUser().imageURL,
            linkURL: getUser().linkURL,
          ),
          SizedBox(
            height: 20,
          ),
          Row(
            children: [
              SizedBox(
                width: MediaQuery.of(context).size.width / 3,
                child: Text(
                  "Username",
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.normal,
                  ),
                ),
              ),
              Expanded(
                child: TextField(
                  style: TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.bold,
                  ),
                  controller: usernameController,
                ),
              ),
              SizedBox(
                width: MediaQuery.of(context).size.width / 10,
                child: Container(
                  color: Colors.blueAccent,
                  child: IconButton(
                      icon: Icon(Icons.arrow_forward, color: Colors.white),
                      onPressed: retrieveUser),
                ),
              ),
            ],
          ),
          SizedBox(
            height: 4,
          ),
          ProfileInfoItem(label: "ID", value: getUser().id),
          SizedBox(
            height: 4,
          ),
          ProfileInfoItem(label: "Gender", value: getUser().gender),
          SizedBox(
            height: 4,
          ),
          ProfileInfoItem(label: "Birthday", value: getUser().birthday),
          SizedBox(
            height: 4,
          ),
          ProfileInfoItem(label: "Location", value: getUser().location),
          SizedBox(
            height: 4,
          ),
          ProfileInfoItem(label: "Last Online", value: getUser().lastOnline),
          SizedBox(
            height: 4,
          ),
          ProfileInfoItem(label: "Joined On", value: getUser().joined),
          SizedBox(
            height: 20,
          ),
          Row(
            children: [
              ElevatedButton(
                onPressed: () {
                  if (username != null) {
                    setState(() {
                      username = null;
                    });
                  }
                },
                child: Text("Log Out"),
              ),
            ],
          ),
        ],
      ),
    ));
  }
}
