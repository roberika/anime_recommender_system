import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

class ProfileImage extends StatefulWidget {
  ProfileImage({super.key, required this.imageURL, required this.linkURL});
  String? imageURL;
  String linkURL;
  @override
  State<ProfileImage> createState() => _ProfileImageState();
}

class _ProfileImageState extends State<ProfileImage> {
  _launchURL() async {
    final Uri _url = Uri.parse(widget.linkURL);
    if (!await launchUrl(_url)) {
      throw Exception('Could not launch $_url');
    }
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _launchURL,
      child: widget.imageURL == null
          ? Image.asset("images/placeholder_profile_picture.jpeg")
          : Image.network(widget.imageURL!),
    );
  }
}
