import 'package:flutter/material.dart';

class ProfileInfoItem extends StatefulWidget {
  ProfileInfoItem({
    super.key,
    required String label,
    String? value
  }) : _label = label, _value = value;

  final String _label;
  String? _value;

  @override
  State<ProfileInfoItem> createState() => _ProfileInfoItemState();
}

class _ProfileInfoItemState extends State<ProfileInfoItem> {
  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        SizedBox(
          width: MediaQuery.of(context).size.width / 3,
          child: Text(
            widget._label,
            style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.normal,
            ),
          ),
        ),
        Expanded(
          child: Text(
            ': ${widget._value}',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,)
          ),
        ),
      ],
    );
  }
}
