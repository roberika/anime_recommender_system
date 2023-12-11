import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:rkmdaa/widgets/profile_image.dart';
import 'package:rkmdaa/widgets/profile_info_item.dart';
import 'package:http/http.dart' as http;

import '../models/user.dart';

class ProfileScreen extends StatefulWidget {
  ProfileScreen({super.key, this.user});
  User? user;

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final TextEditingController usernameController = TextEditingController();
  String? username;

  void retrieveUser() async {
    final response = await http.get(
      Uri.parse(
          'https://api.jikan.moe/v4/users/' + usernameController.value.text),
    );
    if (response.statusCode == 200) {
      setState(() {
        widget.user = User.fromJson(jsonDecode(response.body) as Map<String, dynamic>);
      });
    } else {
      throw Exception('Failed to retrive user.');
    }
    build(context);
  }

  User getUser() {
    if (widget.user == null) {
      return User(
        id: "-",
        username: "",
        imageURL: null,
        linkURL: "https://myanimelist.net/panel.php",
        lastOnline: "-",
        gender: "-",
        birthday: "-",
        location: "-",
        joined: "-",
      );
    } else {
      return widget.user!;
    }
  }

  @override
  Widget build(BuildContext context) {
    usernameController.text = getUser().username;
    return Scaffold(
        body: SingleChildScrollView(
      child: Padding(
        padding: EdgeInsets.only(
            bottom: 16.0,
            left: 16.0,
            right: 16.0,
            top: MediaQuery.of(context).size.height / 6),
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
                Label(label: "Username"),
                Expanded(
                  child: TextField(
                    decoration: InputDecoration.collapsed(
                      hintText: '',
                    ),
                    style: TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.bold,
                    ),
                    controller: usernameController,
                  ),
                ),
                SizedBox(
                  width: MediaQuery.of(context).size.width / 9,
                  child: Container(
                    alignment: Alignment.center,
                    padding: EdgeInsets.zero,
                    color: Colors.blueAccent,
                    height: 20,
                    child: IconButton(
                        padding: EdgeInsets.zero,
                        iconSize: 15,
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
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: () {
                      setState(() {
                        widget.user = null;
                      });
                  },
                  child: Text("Log Out"),
                ),
              ],
            ),
          ],
        ),
      ),
    ));
  }
}
