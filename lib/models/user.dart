class User {
  final String id;
  final String username;
  final String? imageURL;
  final String linkURL;
  final String lastOnline;
  final String gender;
  final String birthday;
  final String location;
  final String joined;

  User({
    required this.id,
    required this.username,
    required this.imageURL,
    required this.linkURL,
    required this.lastOnline,
    required this.gender,
    required this.birthday,
    required this.location,
    required this.joined,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    json = json["data"];
    var user =  User(
              id: json["mal_id"].toString(),
              username: json["username"],
              imageURL: json["images"] == null ? null : json["images"]["jpg"]["image_url"],
              linkURL: json["url"],
              lastOnline: json["last_online"],
              gender: json["gender"] ?? "Unknown",
              birthday: json["birthday"] == null ? "Unknown" : DateTime.parse(json["birthday"])
                  .toLocal()
                  .toString(),
              location: json["location"] ?? "Unknown",
              joined: DateTime.parse(json["joined"]).toLocal().toString());
    return user;
  }
}
