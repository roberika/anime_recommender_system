import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:rkmdaa/main.dart';
import 'package:rkmdaa/widgets/profile_image.dart';
import 'package:rkmdaa/widgets/profile_info_item.dart';
import '../models/user.dart';

class ProfileScreen extends StatefulWidget {
  ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final TextEditingController usernameController = TextEditingController();
  String? username;
  late User user;

  @override
  Widget build(BuildContext context) {
    setState(() {
      user = User.getUser(MainScreen.user);
    });
    usernameController.text = user.username;

    void loadUser() async {
      User? u = await MainScreen.retrieveUser(usernameController.value.text);
      setState(() {
        user = User.getUser(u);
      });
    }

    void unloadUser() {
      MainScreen.user = null;
      MainScreen.recommendations = [];
      MainScreen.history = [];
      setState(() {
        user = User.getUser(null);
      });
    }

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
              imageURL: user.imageURL,
              linkURL: user.linkURL,
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
                        onPressed: loadUser),
                  ),
                ),
              ],
            ),
            SizedBox(
              height: 4,
            ),
            ProfileInfoItem(label: "ID", value: user.id),
            SizedBox(
              height: 4,
            ),
            ProfileInfoItem(label: "Gender", value: user.gender),
            SizedBox(
              height: 4,
            ),
            ProfileInfoItem(label: "Birthday", value: user.birthday),
            SizedBox(
              height: 4,
            ),
            ProfileInfoItem(label: "Location", value: user.location),
            SizedBox(
              height: 4,
            ),
            ProfileInfoItem(label: "Last Online", value: user.lastOnline),
            SizedBox(
              height: 4,
            ),
            ProfileInfoItem(label: "Joined On", value: user.joined),
            SizedBox(
              height: 20,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: unloadUser,
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
