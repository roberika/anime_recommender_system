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
        Label(label: widget._label),
        Expanded(
          child: Text(
            '${widget._value}',
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,)
          ),
        ),
      ],
    );
  }
}

class Label extends StatelessWidget {
  const Label({super.key, required this.label});
  final String label;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        SizedBox(
          width: MediaQuery.of(context).size.width / 4,
          child: Text(
            label,
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.normal,
            ),
          ),
        ),
        Text(": ", style: TextStyle(fontSize: 14),),
      ],
    );
  }
}
