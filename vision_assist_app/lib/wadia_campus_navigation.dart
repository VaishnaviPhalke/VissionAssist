import 'dart:math' as math;
import 'package:flutter/material.dart';

/// Landmark Node on Nowrosjee Wadia College Pune Campus
class WadiaCampusNode {
  final String id;
  final String name;
  final String shortLabel;
  final String category;
  final double x; // Canvas 0..1000
  final double y; // Canvas 0..520
  final double lat;
  final double lon;
  final Color color;
  final Rect? footprint;

  const WadiaCampusNode({
    required this.id,
    required this.name,
    required this.shortLabel,
    required this.category,
    required this.x,
    required this.y,
    required this.lat,
    required this.lon,
    required this.color,
    this.footprint,
  });

  Offset get position => Offset(x, y);
}

/// Navigation Turn-by-Turn Instruction
class WadiaNavInstruction {
  final int stepNumber;
  final String title;
  final String spokenText;
  final String directionType; // 'straight', 'left', 'right', 'arrive'
  final int distanceMeters;
  final Offset mapPoint;
  final double targetLat;
  final double targetLon;

  const WadiaNavInstruction({
    required this.stepNumber,
    required this.title,
    required this.spokenText,
    required this.directionType,
    required this.distanceMeters,
    required this.mapPoint,
    required this.targetLat,
    required this.targetLon,
  });
}

/// Official Wadia College Pune Graph & Routing Engine
class WadiaCampusEngine {
  static const double minLat = 18.5318;
  static const double maxLat = 18.5348;
  static const double minLon = 73.8800;
  static const double maxLon = 73.8855;

  static final List<WadiaCampusNode> nodes = [
    const WadiaCampusNode(
      id: "main_gate",
      name: "Late Prin V.K. Joag Path Main Gate",
      shortLabel: "Main Gate (Joag Path)",
      category: "Entrance",
      x: 475,
      y: 490,
      lat: 18.5320,
      lon: 73.8824,
      color: Color(0xFF2C3E50),
    ),
    const WadiaCampusNode(
      id: "mangaldas_gate",
      name: "Mangaldas Road Entrance Gate",
      shortLabel: "Mangaldas Gate",
      category: "Entrance",
      x: 85,
      y: 100,
      lat: 18.5340,
      lon: 73.8802,
      color: Color(0xFF2C3E50),
    ),
    const WadiaCampusNode(
      id: "bund_garden_gate",
      name: "Bund Garden Side Entrance Gate",
      shortLabel: "Bund Garden Gate",
      category: "Entrance",
      x: 180,
      y: 435,
      lat: 18.5322,
      lon: 73.8808,
      color: Color(0xFF2C3E50),
    ),
    const WadiaCampusNode(
      id: "arts_building",
      name: "Arts (ATRS) Building & Joag Statue",
      shortLabel: "Arts (ATRS) Building",
      category: "Academic",
      x: 525,
      y: 270,
      lat: 18.5334,
      lon: 73.8828,
      color: Color(0xFF1B2A56),
      footprint: Rect.fromLTWH(500, 150, 50, 245),
    ),
    const WadiaCampusNode(
      id: "tata_assembly_hall",
      name: "Tata Assembly Hall & Cusrow Wadia Statue",
      shortLabel: "Tata Assembly Hall",
      category: "Auditorium",
      x: 448,
      y: 270,
      lat: 18.5334,
      lon: 73.8823,
      color: Color(0xFF1B2A56),
      footprint: Rect.fromLTWH(425, 150, 45, 240),
    ),
    const WadiaCampusNode(
      id: "science_building",
      name: "Science Building & College Office",
      shortLabel: "Science Building",
      category: "Academic",
      x: 368,
      y: 270,
      lat: 18.5335,
      lon: 73.8818,
      color: Color(0xFF1B2A56),
      footprint: Rect.fromLTWH(335, 150, 65, 245),
    ),
    const WadiaCampusNode(
      id: "central_library",
      name: "Central Library Building",
      shortLabel: "Central Library",
      category: "Library",
      x: 252,
      y: 165,
      lat: 18.5338,
      lon: 73.8812,
      color: Color(0xFFC2185B),
      footprint: Rect.fromLTWH(210, 145, 85, 40),
    ),
    const WadiaCampusNode(
      id: "admin_building",
      name: "Admin Building & Mechanical Dept",
      shortLabel: "Admin Building",
      category: "Administration",
      x: 252,
      y: 295,
      lat: 18.5332,
      lon: 73.8812,
      color: Color(0xFFC2185B),
      footprint: Rect.fromLTWH(210, 275, 85, 40),
    ),
    const WadiaCampusNode(
      id: "engineering_college",
      name: "Engineering College Building (MESCOE)",
      shortLabel: "MESCOE Engineering",
      category: "Engineering",
      x: 108,
      y: 220,
      lat: 18.5336,
      lon: 73.8803,
      color: Color(0xFFC2185B),
      footprint: Rect.fromLTWH(90, 120, 35, 200),
    ),
    const WadiaCampusNode(
      id: "electronics_workshop",
      name: "Electronics & Workshop Block",
      shortLabel: "Electronics & Workshop",
      category: "Lab",
      x: 155,
      y: 220,
      lat: 18.5335,
      lon: 73.8806,
      color: Color(0xFFC2185B),
      footprint: Rect.fromLTWH(140, 140, 30, 180),
    ),
    const WadiaCampusNode(
      id: "canteen",
      name: "Campus Canteen & CTSE",
      shortLabel: "Campus Canteen",
      category: "Facility",
      x: 368,
      y: 85,
      lat: 18.5346,
      lon: 73.8818,
      color: Color(0xFF00A8FF),
      footprint: Rect.fromLTWH(335, 60, 65, 55),
    ),
    const WadiaCampusNode(
      id: "hostels",
      name: "Boys & Girls Hostels",
      shortLabel: "Hostels",
      category: "Residential",
      x: 210,
      y: 80,
      lat: 18.5347,
      lon: 73.8809,
      color: Color(0xFFE67E22),
      footprint: Rect.fromLTWH(115, 60, 190, 40),
    ),
    const WadiaCampusNode(
      id: "junior_college_office",
      name: "Junior College Office",
      shortLabel: "Jr College Office",
      category: "Office",
      x: 450,
      y: 90,
      lat: 18.5346,
      lon: 73.8823,
      color: Color(0xFF1B2A56),
      footprint: Rect.fromLTWH(430, 70, 40, 40),
    ),
    const WadiaCampusNode(
      id: "ness_wadia",
      name: "Ness Wadia College & Neville Wadia IMR",
      shortLabel: "Ness Wadia College",
      category: "Academic",
      x: 772,
      y: 95,
      lat: 18.5345,
      lon: 73.8842,
      color: Color(0xFF7B241C),
      footprint: Rect.fromLTWH(720, 70, 105, 50),
    ),
    const WadiaCampusNode(
      id: "open_air_theatre",
      name: "Open Air Theatre",
      shortLabel: "Open Air Theatre",
      category: "Cultural",
      x: 855,
      y: 115,
      lat: 18.5344,
      lon: 73.8848,
      color: Color(0xFF26A69A),
      footprint: Rect.fromLTWH(830, 95, 50, 40),
    ),
    const WadiaCampusNode(
      id: "playground_pavilion",
      name: "Play Ground & Gymkhana Pavilion",
      shortLabel: "Play Ground & Gymkhana",
      category: "Sports",
      x: 750,
      y: 310,
      lat: 18.5330,
      lon: 73.8842,
      color: Color(0xFF27AE60),
    ),
    const WadiaCampusNode(
      id: "parking_area",
      name: "Campus Central Parking",
      shortLabel: "Parking Area",
      category: "Parking",
      x: 440,
      y: 438,
      lat: 18.5323,
      lon: 73.8822,
      color: Color(0xFFB0BEC5),
      footprint: Rect.fromLTWH(320, 395, 245, 85),
    ),
    const WadiaCampusNode(
      id: "bank_post_office",
      name: "Bank & Post Office",
      shortLabel: "Bank & Post Office",
      category: "Service",
      x: 160,
      y: 368,
      lat: 18.5326,
      lon: 73.8806,
      color: Color(0xFF8D6E63),
      footprint: Rect.fromLTWH(145, 350, 30, 35),
    ),
  ];

  static final Map<String, List<String>> adjacency = {
    "main_gate": ["parking_area"],
    "parking_area": ["main_gate", "tata_assembly_hall", "arts_building", "science_building"],
    "bund_garden_gate": ["bank_post_office"],
    "bank_post_office": ["bund_garden_gate", "admin_building"],
    "mangaldas_gate": ["engineering_college"],
    "engineering_college": ["mangaldas_gate", "electronics_workshop", "hostels"],
    "electronics_workshop": ["engineering_college", "central_library", "admin_building"],
    "central_library": ["electronics_workshop", "admin_building", "canteen"],
    "admin_building": ["central_library", "science_building", "bank_post_office"],
    "hostels": ["engineering_college", "canteen"],
    "canteen": ["hostels", "central_library", "junior_college_office", "science_building"],
    "junior_college_office": ["canteen", "tata_assembly_hall", "ness_wadia"],
    "science_building": ["canteen", "admin_building", "tata_assembly_hall", "parking_area"],
    "tata_assembly_hall": ["science_building", "arts_building", "junior_college_office", "parking_area"],
    "arts_building": ["tata_assembly_hall", "parking_area", "playground_pavilion"],
    "ness_wadia": ["junior_college_office", "open_air_theatre", "playground_pavilion"],
    "open_air_theatre": ["ness_wadia"],
    "playground_pavilion": ["arts_building", "ness_wadia"],
  };

  static WadiaCampusNode? getNodeById(String id) {
    try {
      return nodes.firstWhere((n) => n.id == id);
    } catch (_) {
      return null;
    }
  }

  static WadiaCampusNode? getNodeByName(String name) {
    try {
      return nodes.firstWhere((n) => n.name == name || n.shortLabel == name);
    } catch (_) {
      return null;
    }
  }

  /// Convert GPS Coordinates to Canvas (X, Y)
  static Offset gpsToCanvas(double lat, double lon) {
    final clampedLat = lat.clamp(minLat, maxLat);
    final clampedLon = lon.clamp(minLon, maxLon);
    final normX = (clampedLon - minLon) / (maxLon - minLon);
    final normY = (maxLat - clampedLat) / (maxLat - minLat); // Invert Y
    return Offset(normX * 1000.0, normY * 520.0);
  }

  /// Convert Canvas (X, Y) to GPS Coordinates
  static Map<String, double> canvasToGps(double x, double y) {
    final normX = (x / 1000.0).clamp(0.0, 1.0);
    final normY = (y / 520.0).clamp(0.0, 1.0);
    final lon = minLon + normX * (maxLon - minLon);
    final lat = maxLat - normY * (maxLat - minLat);
    return {'lat': lat, 'lon': lon};
  }

  /// Calculate shortest step-free path using BFS / Dijkstra
  static List<WadiaNavInstruction> calculateRoute(String startId, String endId) {
    if (startId == endId) {
      final node = getNodeById(startId) ?? nodes.first;
      return [
        WadiaNavInstruction(
          stepNumber: 1,
          title: "You are already at ${node.shortLabel}",
          spokenText: "You are already at ${node.name}.",
          directionType: "arrive",
          distanceMeters: 0,
          mapPoint: node.position,
          targetLat: node.lat,
          targetLon: node.lon,
        )
      ];
    }

    final queue = <List<String>>[[startId]];
    final visited = <String>{startId};
    List<String>? shortestPath;

    while (queue.isNotEmpty) {
      final path = queue.removeAt(0);
      final current = path.last;

      if (current == endId) {
        shortestPath = path;
        break;
      }

      final neighbors = adjacency[current] ?? [];
      for (final neighbor in neighbors) {
        if (!visited.contains(neighbor)) {
          visited.add(neighbor);
          final newPath = List<String>.from(path)..add(neighbor);
          queue.add(newPath);
        }
      }
    }

    if (shortestPath == null || shortestPath.length < 2) {
      final endNode = getNodeById(endId) ?? nodes.last;
      return [
        WadiaNavInstruction(
          stepNumber: 1,
          title: "Proceed directly towards ${endNode.shortLabel}",
          spokenText: "Proceed along accessible internal road towards ${endNode.name}.",
          directionType: "straight",
          distanceMeters: 50,
          mapPoint: endNode.position,
          targetLat: endNode.lat,
          targetLon: endNode.lon,
        )
      ];
    }

    final instructions = <WadiaNavInstruction>[];
    for (int i = 0; i < shortestPath.length; i++) {
      final currNode = getNodeById(shortestPath[i])!;
      if (i == 0) {
        final nextNode = getNodeById(shortestPath[i + 1])!;
        final dist = _approxDistanceMeters(currNode, nextNode);
        instructions.add(WadiaNavInstruction(
          stepNumber: 1,
          title: "Depart ${currNode.shortLabel} along accessible corridor",
          spokenText: "Starting step-free route from ${currNode.name}. Walk towards ${nextNode.shortLabel} for $dist meters.",
          directionType: "straight",
          distanceMeters: dist,
          mapPoint: currNode.position,
          targetLat: currNode.lat,
          targetLon: currNode.lon,
        ));
      } else if (i == shortestPath.length - 1) {
        instructions.add(WadiaNavInstruction(
          stepNumber: i + 1,
          title: "Arrive at ${currNode.shortLabel}",
          spokenText: "You have arrived at ${currNode.name}. The entrance ramp is immediately ahead.",
          directionType: "arrive",
          distanceMeters: 0,
          mapPoint: currNode.position,
          targetLat: currNode.lat,
          targetLon: currNode.lon,
        ));
      } else {
        final prevNode = getNodeById(shortestPath[i - 1])!;
        final nextNode = getNodeById(shortestPath[i + 1])!;
        final turn = _getTurnDirection(prevNode, currNode, nextNode);
        final dist = _approxDistanceMeters(currNode, nextNode);

        instructions.add(WadiaNavInstruction(
          stepNumber: i + 1,
          title: "$turn towards ${nextNode.shortLabel}",
          spokenText: "$turn towards ${nextNode.shortLabel}. Continue straight for $dist meters.",
          directionType: turn.toLowerCase().contains("left") ? "left" : "right",
          distanceMeters: dist,
          mapPoint: currNode.position,
          targetLat: currNode.lat,
          targetLon: currNode.lon,
        ));
      }
    }

    return instructions;
  }

  static int _approxDistanceMeters(WadiaCampusNode a, WadiaCampusNode b) {
    final dx = (a.x - b.x);
    final dy = (a.y - b.y);
    final pixelDist = math.sqrt(dx * dx + dy * dy);
    // 1000 canvas pixels approx 380 meters
    return (pixelDist * 0.38).round().clamp(10, 200);
  }

  static String _getTurnDirection(WadiaCampusNode prev, WadiaCampusNode curr, WadiaCampusNode next) {
    final dx1 = curr.x - prev.x;
    final dy1 = curr.y - prev.y;
    final dx2 = next.x - curr.x;
    final dy2 = next.y - curr.y;

    final crossProduct = dx1 * dy2 - dy1 * dx2;
    if (crossProduct > 200) {
      return "Turn Right";
    } else if (crossProduct < -200) {
      return "Turn Left";
    } else {
      return "Continue Straight";
    }
  }
}

/// High-Fidelity CustomPainter for Nowrosjee Wadia College Pune Layout
class WadiaCampusMapPainter extends CustomPainter {
  final List<Offset> routePolyline;
  final Offset? userLocation;
  final double userHeading;
  final String? activeWaypointNodeId;
  final String? destinationNodeId;

  WadiaCampusMapPainter({
    required this.routePolyline,
    this.userLocation,
    this.userHeading = 0.0,
    this.activeWaypointNodeId,
    this.destinationNodeId,
  });

  @override
  void paint(Canvas canvas, Size size) {
    final scaleX = size.width / 1000.0;
    final scaleY = size.height / 520.0;

    canvas.save();
    canvas.scale(scaleX, scaleY);

    // 1. Campus Ground Background
    final bgPaint = Paint()..color = const Color(0xFFF4F6F9);
    canvas.drawRect(const Rect.fromLTWH(0, 0, 1000, 520), bgPaint);

    // 2. Play Ground (Large Oval & Running Track)
    final trackCenter = const Offset(755, 310);
    final trackPaint = Paint()
      ..color = const Color(0xFFFF6584)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 24.0;
    canvas.drawOval(Rect.fromCenter(center: trackCenter, width: 330, height: 230), trackPaint);

    final grassPaint = Paint()..color = const Color(0xFF27AE60);
    canvas.drawOval(Rect.fromCenter(center: trackCenter, width: 300, height: 200), grassPaint);

    // Play Ground Center Circle
    final centerLinePaint = Paint()
      ..color = Colors.white.withOpacity(0.4)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;
    canvas.drawCircle(trackCenter, 40, centerLinePaint);

    _drawText(canvas, "PLAY GROUND", const Offset(755, 305), Colors.white, fontSize: 13, isBold: true, alignCenter: true);

    // 3. Roads & Internal Paths
    _drawRoads(canvas);

    // 4. Campus Central Parking
    _drawParkingArea(canvas);

    // 5. Buildings Matching Layout Colors
    _drawBuildings(canvas);

    // 6. Statues & Landmarks
    _drawLandmarks(canvas);

    // 7. Active Navigation Route Polyline
    if (routePolyline.length > 1) {
      _drawNavigationRoute(canvas);
    }

    // 8. Live User Location Pin & Radar
    if (userLocation != null) {
      _drawUserLocationPin(canvas, userLocation!);
    }

    canvas.restore();
  }

  void _drawRoads(Canvas canvas) {
    final roadPaint = Paint()
      ..color = const Color(0xFF455A64)
      ..style = PaintingStyle.fill;

    final internalRoadPaint = Paint()
      ..color = const Color(0xFF90A4AE)
      ..style = PaintingStyle.fill;

    final dashPaint = Paint()
      ..color = Colors.white70
      ..strokeWidth = 2.0;

    // Late Prin. V. K. Joag Path (Bottom)
    canvas.drawRect(const Rect.fromLTWH(0, 485, 1000, 35), roadPaint);
    for (double x = 10; x < 990; x += 30) {
      canvas.drawLine(Offset(x, 502), Offset(x + 15, 502), dashPaint);
    }
    _drawText(canvas, "LATE PRIN. V. K. JOAG PATH", const Offset(500, 495), Colors.white, fontSize: 11, isBold: true, alignCenter: true);
    _drawText(canvas, "ENT GATE", const Offset(475, 475), const Color(0xFF1B2A56), fontSize: 9, isBold: true, alignCenter: true);
    _drawText(canvas, "TO BUND GARDEN →", const Offset(190, 473), const Color(0xFF1B2A56), fontSize: 9, isBold: true);

    // Mangaldas Road (West angled path)
    final mangaldasPath = Path()
      ..moveTo(80, 0)
      ..lineTo(112, 0)
      ..lineTo(60, 360)
      ..lineTo(190, 485)
      ..lineTo(158, 485)
      ..lineTo(28, 360)
      ..close();
    canvas.drawPath(mangaldasPath, roadPaint);
    _drawText(canvas, "MANGALDAS ROAD", const Offset(55, 180), Colors.white, fontSize: 10, isBold: true, rotation: 1.45);
    _drawText(canvas, "ENT GATE", const Offset(70, 95), Colors.white, fontSize: 8, isBold: true);

    // 9.00 M Wide Internal Road (Top East-West)
    canvas.drawRect(const Rect.fromLTWH(90, 115, 600, 20), internalRoadPaint);
    _drawText(canvas, "9.00 M WIDE INTERNAL ROAD", const Offset(390, 120), Colors.white, fontSize: 9, isBold: true, alignCenter: true);

    // 6.00 M Wide Internal Road (Vertical next to Arts/Playground)
    canvas.drawRect(const Rect.fromLTWH(570, 120, 18, 275), internalRoadPaint);
    _drawText(canvas, "6.00 M INTERNAL ROAD", const Offset(580, 250), Colors.white, fontSize: 8, isBold: true, rotation: 1.57);

    // 6.00 M Wide Internal Road (Horizontal above Parking)
    canvas.drawRect(const Rect.fromLTWH(300, 395, 288, 16), internalRoadPaint);

    // Internal Road (Between Admin and Science)
    canvas.drawRect(const Rect.fromLTWH(180, 320, 155, 16), internalRoadPaint);

    // Railway line on East perimeter
    final railPaint = Paint()
      ..color = const Color(0xFF78909C)
      ..strokeWidth = 3.0;
    canvas.drawLine(const Offset(985, 0), const Offset(985, 520), railPaint);
    canvas.drawLine(const Offset(993, 0), const Offset(993, 520), railPaint);
    for (double y = 10; y < 510; y += 14) {
      canvas.drawLine(Offset(982, y), Offset(996, y), Paint()..color = const Color(0xFF546E7A)..strokeWidth = 1.5);
    }
    _drawText(canvas, "RAILWAY LINE", const Offset(968, 260), const Color(0xFF37474F), fontSize: 9, isBold: true, rotation: 1.57);
  }

  void _drawParkingArea(Canvas canvas) {
    const parkingRect = Rect.fromLTWH(320, 415, 245, 65);
    canvas.drawRect(parkingRect, Paint()..color = const Color(0xFFE2E7EC));
    canvas.drawRect(parkingRect, Paint()..color = const Color(0xFF90A4AE)..style = PaintingStyle.stroke..strokeWidth = 1.5);

    // Diagonal parking slots
    final stripePaint = Paint()..color = Colors.white70..strokeWidth = 1.5;
    for (double x = 325; x < 560; x += 18) {
      canvas.drawLine(Offset(x, 415), Offset(x + 10, 480), stripePaint);
    }
    _drawText(canvas, "CAMPUS PARKING", const Offset(442, 442), const Color(0xFF455A64), fontSize: 11, isBold: true, alignCenter: true);
  }

  void _drawBuildings(Canvas canvas) {
    for (final node in WadiaCampusEngine.nodes) {
      if (node.footprint == null) continue;

      final rect = node.footprint!;
      final rrect = RRect.fromRectAndRadius(rect, const Radius.circular(5));

      // Building Fill
      final fillPaint = Paint()..color = node.color;
      canvas.drawRRect(rrect, fillPaint);

      // Building Outline
      final strokePaint = Paint()
        ..color = Colors.black26
        ..style = PaintingStyle.stroke
        ..strokeWidth = 1.2;
      canvas.drawRRect(rrect, strokePaint);

      // Label
      final textColor = (node.color == const Color(0xFFB0BEC5) || node.color == const Color(0xFFE2E7EC))
          ? Colors.black87
          : Colors.white;

      _drawText(
        canvas,
        node.shortLabel,
        Offset(rect.center.dx, rect.center.dy - 5),
        textColor,
        fontSize: rect.width < 50 ? 8 : 10,
        isBold: true,
        alignCenter: true,
      );
    }

    // Additional specific buildings matching the layout:
    // Electronics building
    final elecRect = const Rect.fromLTWH(140, 215, 28, 105);
    canvas.drawRect(elecRect, Paint()..color = const Color(0xFFC2185B));
    canvas.drawRect(elecRect, Paint()..color = Colors.black26..style = PaintingStyle.stroke);
    _drawText(canvas, "ELECTRONICS", const Offset(154, 260), Colors.white, fontSize: 7, isBold: true, rotation: 1.57, alignCenter: true);

    // Workshop
    final workRect = const Rect.fromLTWH(140, 140, 30, 45);
    canvas.drawRect(workRect, Paint()..color = const Color(0xFFC2185B));
    canvas.drawRect(workRect, Paint()..color = Colors.black26..style = PaintingStyle.stroke);
    _drawText(canvas, "WORK SHOP", const Offset(155, 158), Colors.white, fontSize: 7, isBold: true, alignCenter: true);

    // Neville Wadia IMR
    final nevilleRect = const Rect.fromLTWH(640, 75, 75, 35);
    canvas.drawRect(nevilleRect, Paint()..color = const Color(0xFFB2D235));
    canvas.drawRect(nevilleRect, Paint()..color = Colors.black26..style = PaintingStyle.stroke);
    _drawText(canvas, "NEVILLE WADIA", const Offset(677, 90), Colors.black87, fontSize: 8, isBold: true, alignCenter: true);

    // Pavilion & Gymkhana
    final pavRect = const Rect.fromLTWH(860, 410, 110, 65);
    canvas.drawRect(pavRect, Paint()..color = const Color(0xFFD32F2F));
    canvas.drawRect(pavRect, Paint()..color = Colors.black26..style = PaintingStyle.stroke);
    _drawText(canvas, "PAVILION & GYMKHANA", const Offset(915, 438), Colors.white, fontSize: 8, isBold: true, alignCenter: true);

    // Botanical Garden & Staff Quarters
    final gardenRect = const Rect.fromLTWH(280, 375, 16, 55);
    canvas.drawRect(gardenRect, Paint()..color = const Color(0xFF4CAF50));
    _drawText(canvas, "GARDEN", const Offset(288, 400), Colors.white, fontSize: 6, isBold: true, rotation: 1.57, alignCenter: true);

    final quartersRect = const Rect.fromLTWH(230, 375, 20, 65);
    canvas.drawRect(quartersRect, Paint()..color = const Color(0xFF1E824C));
    _drawText(canvas, "STAFF", const Offset(240, 405), Colors.white, fontSize: 6, isBold: true, rotation: 1.57, alignCenter: true);
  }

  void _drawLandmarks(Canvas canvas) {
    // Cusrow Wadia Statue
    final cusrowPos = const Offset(448, 410);
    canvas.drawCircle(cusrowPos, 6, Paint()..color = const Color(0xFFFFB300));
    canvas.drawCircle(cusrowPos, 3, Paint()..color = Colors.black);
    _drawText(canvas, "Cusrow Wadia Statue", const Offset(448, 400), const Color(0xFF1B2A56), fontSize: 8, isBold: true, alignCenter: true);

    // V.K. Joag Statue & YOU ARE HERE
    final joagPos = const Offset(550, 350);
    canvas.drawCircle(joagPos, 6, Paint()..color = const Color(0xFFE53935));
    canvas.drawCircle(joagPos, 3, Paint()..color = Colors.white);
    _drawText(canvas, "V.K. Joag Statue", const Offset(550, 360), const Color(0xFFC62828), fontSize: 8, isBold: true, alignCenter: true);

    // Compass Indicator on North-East
    final compassCenter = const Offset(960, 40);
    canvas.drawCircle(compassCenter, 18, Paint()..color = Colors.white..style = PaintingStyle.fill);
    canvas.drawCircle(compassCenter, 18, Paint()..color = const Color(0xFF1B2A56)..style = PaintingStyle.stroke..strokeWidth = 2);
    _drawText(canvas, "N", const Offset(960, 32), const Color(0xFF1B2A56), fontSize: 13, isBold: true, alignCenter: true);
    // Arrow pointing East/Right (official orientation)
    final arrowPath = Path()
      ..moveTo(968, 40)
      ..lineTo(952, 34)
      ..lineTo(952, 46)
      ..close();
    canvas.drawPath(arrowPath, Paint()..color = const Color(0xFF1B2A56));
  }

  void _drawNavigationRoute(Canvas canvas) {
    final path = Path();
    path.moveTo(routePolyline.first.dx, routePolyline.first.dy);
    for (int i = 1; i < routePolyline.length; i++) {
      path.lineTo(routePolyline[i].dx, routePolyline[i].dy);
    }

    // Outer Glow
    final glowPaint = Paint()
      ..color = const Color(0xFF00E5FF).withOpacity(0.5)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 10.0
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round;
    canvas.drawPath(path, glowPaint);

    // Core Solid Path
    final corePaint = Paint()
      ..color = const Color(0xFF0C8B74)
      ..style = PaintingStyle.stroke
      ..strokeWidth = 5.0
      ..strokeCap = StrokeCap.round
      ..strokeJoin = StrokeJoin.round;
    canvas.drawPath(path, corePaint);

    // Waypoint Dots
    for (final pt in routePolyline) {
      canvas.drawCircle(pt, 6.0, Paint()..color = Colors.white);
      canvas.drawCircle(pt, 4.0, Paint()..color = const Color(0xFF0C8B74));
    }

    // Destination Pin
    final dest = routePolyline.last;
    canvas.drawCircle(dest, 10.0, Paint()..color = const Color(0xFFE53935));
    canvas.drawCircle(dest, 5.0, Paint()..color = Colors.white);
  }

  void _drawUserLocationPin(Canvas canvas, Offset pos) {
    // Pulsing radar ring
    canvas.drawCircle(pos, 22.0, Paint()..color = const Color(0xFF00A8FF).withOpacity(0.25));
    canvas.drawCircle(pos, 14.0, Paint()..color = const Color(0xFF00A8FF).withOpacity(0.4));

    // Heading cone
    if (userHeading != 0.0) {
      final rad = (userHeading - 90) * math.pi / 180.0;
      final conePath = Path()
        ..moveTo(pos.dx, pos.dy)
        ..lineTo(pos.dx + 25 * math.cos(rad - 0.4), pos.dy + 25 * math.sin(rad - 0.4))
        ..lineTo(pos.dx + 30 * math.cos(rad), pos.dy + 30 * math.sin(rad))
        ..lineTo(pos.dx + 25 * math.cos(rad + 0.4), pos.dy + 25 * math.sin(rad + 0.4))
        ..close();
      canvas.drawPath(conePath, Paint()..color = const Color(0xFF00A8FF).withOpacity(0.35));
    }

    // Center Blue Dot
    canvas.drawCircle(pos, 8.0, Paint()..color = Colors.white);
    canvas.drawCircle(pos, 6.0, Paint()..color = const Color(0xFF0066FF));

    // Live Badge above avatar
    final badgeRect = Rect.fromCenter(center: Offset(pos.dx, pos.dy - 20), width: 72, height: 16);
    canvas.drawRRect(RRect.fromRectAndRadius(badgeRect, const Radius.circular(8)), Paint()..color = const Color(0xFF0C8B74));
    _drawText(canvas, "LIVE GPS YOU", Offset(pos.dx, pos.dy - 25), Colors.white, fontSize: 8, isBold: true, alignCenter: true);
  }

  void _drawText(
    Canvas canvas,
    String text,
    Offset offset,
    Color color, {
    double fontSize = 10,
    bool isBold = false,
    bool alignCenter = false,
    double rotation = 0.0,
  }) {
    final textSpan = TextSpan(
      text: text,
      style: TextStyle(
        color: color,
        fontSize: fontSize,
        fontWeight: isBold ? FontWeight.bold : FontWeight.normal,
        shadows: const [
          Shadow(color: Colors.black45, blurRadius: 2, offset: Offset(0.5, 0.5)),
        ],
      ),
    );

    final textPainter = TextPainter(
      text: textSpan,
      textDirection: TextDirection.ltr,
    );
    textPainter.layout();

    canvas.save();
    if (rotation != 0.0) {
      canvas.translate(offset.dx, offset.dy);
      canvas.rotate(rotation);
      final dx = alignCenter ? -textPainter.width / 2 : 0.0;
      final dy = alignCenter ? -textPainter.height / 2 : 0.0;
      textPainter.paint(canvas, Offset(dx, dy));
    } else {
      final dx = alignCenter ? offset.dx - textPainter.width / 2 : offset.dx;
      final dy = alignCenter ? offset.dy - textPainter.height / 2 : offset.dy;
      textPainter.paint(canvas, Offset(dx, dy));
    }
    canvas.restore();
  }

  @override
  bool shouldRepaint(covariant WadiaCampusMapPainter oldDelegate) {
    return oldDelegate.routePolyline != routePolyline ||
        oldDelegate.userLocation != userLocation ||
        oldDelegate.userHeading != userHeading ||
        oldDelegate.activeWaypointNodeId != activeWaypointNodeId;
  }
}
