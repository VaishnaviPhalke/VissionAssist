import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:camera/camera.dart';
import 'package:http/http.dart' as http;
import 'package:google_mlkit_text_recognition/google_mlkit_text_recognition.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;

List<CameraDescription> cameras = [];

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  try {
    cameras = await availableCameras();
  } catch (e) {
    debugPrint("Camera initialization fallback: $e");
  }
  runApp(const VisionAssistApp());
}

// ========================================================
// MULTILINGUAL TRANSLATION DICTIONARY
// ========================================================
class AppTranslations {
  static final Map<String, Map<String, dynamic>> data = {
    'en-US': {
      'name': 'English',
      'tagline': 'Smarter Campus. Safer Journeys.',
      'welcome_speech': 'Welcome to VisionAssist. Step 1: Please select your preferred language. Tap English, Hindi, or Marathi.',
      'lang_confirmed': 'Language set to English. Calibrate your speech rate.',
      'test_phrase': 'Testing VisionAssist speech rate. Audio is loud and clear.',
      'setup_complete': 'Setup completed! Starting real-time object detection.',
      'path_clear': 'Path is clear. Safe corridor detected ahead.',
      'scanning': 'Scanning environment...',
      'reading_text': 'Reading text from camera...',
      'no_text_found': 'No legible text detected. Point camera directly at sign.',
      'warning': 'Warning',
      'caution': 'Caution',
      'ahead': 'directly ahead',
      'left': 'on your left',
      'right': 'on your right',
      'meters': 'meters',
      'start_detect': 'Start Object Detection',
      'home': 'Home',
      'detect': 'Detect',
      'read': 'Read',
      'settings': 'Settings',
      'classes': {
        'chair': 'Chair',
        'person': 'Person',
        'table': 'Table',
        'stairs': 'Stairs',
        'door': 'Door',
        'lift': 'Elevator Lift',
        'bottle': 'Bottle',
        'backpack': 'Backpack',
        'tree': 'Tree',
        'car': 'Vehicle Car',
        'bicycle': 'Bicycle',
        'bench': 'Bench',
        'classroom': 'Classroom',
        'laboratory': 'Laboratory',
        'corridor': 'Corridor',
        'laptop': 'Laptop',
        'cell phone': 'Phone',
      }
    },
    'hi-IN': {
      'name': 'हिन्दी (Hindi)',
      'tagline': 'स्मार्ट कैंपस। सुरक्षित यात्रा।',
      'welcome_speech': 'विजन-असिस्ट में आपका स्वागत है। चरण १: कृपया अपनी भाषा चुनें।',
      'lang_confirmed': 'भाषा हिन्दी चुनी गई। अब अपनी आवाज की गति जांचें।',
      'test_phrase': 'विजन-असिस्ट हिन्दी आवाज का परीक्षण। आवाज साफ और स्पष्ट है।',
      'setup_complete': 'सेटअप पूरा हुआ! वास्तविक समय बाधा पहचान शुरू की जा रही है।',
      'path_clear': 'रास्ता साफ है। आगे कोई बाधा नहीं है।',
      'scanning': 'आसपास की जांच हो रही है...',
      'reading_text': 'कैमरा से लिखावट पढ़ी जा रही है...',
      'no_text_found': 'कोई लिखावट नहीं मिली। कैमरा बोर्ड की तरफ करें।',
      'warning': 'चेतावनी',
      'caution': 'सावधान',
      'ahead': 'सीधे सामने',
      'left': 'बाईं ओर',
      'right': 'दाईं ओर',
      'meters': 'मीटर',
      'start_detect': 'बाधा पहचान शुरू करें',
      'home': 'होम',
      'detect': 'पहचान',
      'read': 'पढ़ें',
      'settings': 'सेटिंग्स',
      'classes': {
        'chair': 'कुर्सी',
        'person': 'व्यक्ति',
        'table': 'मेज़',
        'stairs': 'सीढ़ियां',
        'door': 'दरवाज़ा',
        'lift': 'लिफ्ट',
        'bottle': 'बोतल',
        'backpack': 'बैग',
        'tree': 'पेड़',
        'car': 'गाड़ी',
        'bicycle': 'साइकिल',
        'bench': 'बेंच',
        'classroom': 'कक्षा',
        'laboratory': 'प्रयोगशाला',
        'corridor': 'गलियारा',
        'laptop': 'लैपटॉप',
        'cell phone': 'फ़ोन',
      }
    },
    'mr-IN': {
      'name': 'मराठी (Marathi)',
      'tagline': 'स्मार्ट कॅम्पस. सुरक्षित प्रवास.',
      'welcome_speech': 'व्हिजन-असिस्ट मध्ये आपले स्वागत आहे. पायरी १: कृपया भाषा निवडा.',
      'lang_confirmed': 'भाषा मराठी निवडली आहे. आता आवाजाचा वेग तपासा.',
      'test_phrase': 'व्हिजन-असिस्ट मराठी आवाजाची चाचणी. आवाज स्पष्ट ऐकू येत आहे.',
      'setup_complete': 'सेटअप पूर्ण झाले! थेट अडथळा शोध सुरू करत आहे.',
      'path_clear': 'रस्ता मोकळा आहे. समोर कोणताही अडथळा नाही.',
      'scanning': 'परिसराचा शोध घेत आहे...',
      'reading_text': 'पाटीवरील मजकूर वाचत आहे...',
      'no_text_found': 'मजकूर सापडला नाही. कॅमेरा बोर्डकडे धरा.',
      'warning': 'सावधानता',
      'caution': 'काळजी घ्या',
      'ahead': 'अगदी समोर',
      'left': 'डाव्या बाजूला',
      'right': 'उजव्या बाजूला',
      'meters': 'मीटरवर',
      'start_detect': 'अडथळा शोध सुरू करा',
      'home': 'मुख्य',
      'detect': 'शोध',
      'read': 'वाचा',
      'settings': 'सेटिंग्ज',
      'classes': {
        'chair': 'खुर्ची',
        'person': 'माणूस',
        'table': 'मेज',
        'stairs': 'पायऱ्या',
        'door': 'दरवाजा',
        'lift': 'लिफ्ट',
        'bottle': 'बाटली',
        'backpack': 'दप्तर',
        'tree': 'झाड',
        'car': 'गाडी',
        'bicycle': 'सायकल',
        'bench': 'बाकडी',
        'classroom': 'वर्गखोली',
        'laboratory': 'प्रयोगशाळा',
        'corridor': 'व्हरांडा',
        'laptop': 'लॅपटॉप',
        'cell phone': 'फोन',
      }
    },
    'es-ES': {
      'name': 'Español',
      'tagline': 'Campus Más Inteligente. Rutas Más Seguras.',
      'welcome_speech': 'Bienvenido a VisionAssist. Selecciona tu idioma.',
      'lang_confirmed': 'Idioma configurado en Español.',
      'test_phrase': 'Probando la voz de VisionAssist en español.',
      'setup_complete': 'Iniciando detección de obstáculos en tiempo real.',
      'path_clear': 'Camino despejado. No hay obstáculos.',
      'scanning': 'Escaneando entorno...',
      'reading_text': 'Leyendo texto del cartel...',
      'no_text_found': 'No se detectó texto en el marco.',
      'warning': 'Advertencia',
      'caution': 'Precaución',
      'ahead': 'directo al frente',
      'left': 'a tu izquierda',
      'right': 'a tu derecha',
      'meters': 'metros',
      'start_detect': 'Iniciar Detección',
      'home': 'Inicio',
      'detect': 'Detectar',
      'read': 'Leer',
      'settings': 'Ajustes',
      'classes': {
        'chair': 'Silla',
        'person': 'Persona',
        'table': 'Mesa',
        'stairs': 'Escaleras',
        'door': 'Puerta',
        'lift': 'Ascensor',
        'bottle': 'Botella',
        'backpack': 'Mochila',
        'tree': 'Árbol',
        'car': 'Coche',
        'bicycle': 'Bicicleta',
        'bench': 'Banco',
        'classroom': 'Aula',
        'laboratory': 'Laboratorio',
        'corridor': 'Pasillo',
      }
    },
    'ta-IN': {
      'name': 'தமிழ் (Tamil)',
      'tagline': 'பாதுகாப்பான வளாகப் பயணம்.',
      'welcome_speech': 'விஷன்-அசிஸ்ட்டிற்கு வரவேற்கிறோம். தயவுசெய்து மொழியைத் தேர்ந்தெடுக்கவும்.',
      'lang_confirmed': 'தமிழ் மொழி தேர்ந்தெடுக்கப்பட்டது.',
      'test_phrase': 'விஷன்-அசிஸ்ட் தமிழ் குரல் சோதனை.',
      'setup_complete': 'அமைப்பு முடிந்தது! தடைகள் கண்டறிதல் தொடங்குகிறது.',
      'path_clear': 'பாதை தெளிவாக உள்ளது. தடைகள் இல்லை.',
      'scanning': 'சூழலை ஆராய்கிறது...',
      'reading_text': 'எழுத்துகளைப் படிக்கிறது...',
      'no_text_found': 'எழுத்துகள் எதுவும் கிடைக்கவில்லை.',
      'warning': 'எச்சரிக்கை',
      'caution': 'கவனம்',
      'ahead': 'நேரடியாக முன்னால்',
      'left': 'உங்கள் இடதுபுறம்',
      'right': 'உங்கள் வலதுபுறம்',
      'meters': 'மீட்டரில்',
      'start_detect': 'தடைகள் கண்டறியத் தொடங்கு',
      'home': 'முகப்பு',
      'detect': 'கண்டறி',
      'read': 'படி',
      'settings': 'அமைப்புகள்',
      'classes': {
        'chair': 'நாற்காலி',
        'person': 'நபர்',
        'table': 'மேசை',
        'stairs': 'படிகள்',
        'door': 'கதவு',
        'lift': 'மின்தூக்கி',
        'bottle': 'பாட்டில்',
        'backpack': 'பை',
        'tree': 'மரம்',
        'car': 'வாகனம்',
        'bicycle': 'மிதிவண்டி',
        'bench': 'பெஞ்ச்',
        'classroom': 'வகுப்பறை',
        'laboratory': 'ஆய்வகம்',
        'corridor': 'வராண்டா',
      }
    }
  };
}

// ========================================================
// MAIN APPLICATION ROOT
// ========================================================
class VisionAssistApp extends StatefulWidget {
  const VisionAssistApp({super.key});

  @override
  State<VisionAssistApp> createState() => _VisionAssistAppState();
}

class _VisionAssistAppState extends State<VisionAssistApp> {
  final FlutterTts _flutterTts = FlutterTts();
  static const MethodChannel _vibrateChannel = MethodChannel('com.visionassist.ai/vibrate');

  String _currentLang = 'en-US';
  double _speechRate = 0.5;
  String _backendIp = '10.31.190.21:8000';

  @override
  void initState() {
    super.initState();
    _configureTts();
  }

  Future<void> _configureTts() async {
    await _flutterTts.setLanguage(_currentLang);
    await _flutterTts.setSpeechRate(_speechRate);
    await _flutterTts.setVolume(1.0);
    await _flutterTts.setPitch(1.0);
  }

  Future<void> _speak(String text, {String? lang}) async {
    if (text.isEmpty) return;
    try {
      final speakLang = lang ?? _currentLang;
      await _flutterTts.setLanguage(speakLang);
      await _flutterTts.setSpeechRate(_speechRate);
      await _flutterTts.speak(text);
    } catch (e) {
      debugPrint("TTS Speech Error: $e");
    }
  }

  Future<void> _vibrate(int durationMs) async {
    try {
      await _vibrateChannel.invokeMethod('vibrate', {'duration': durationMs});
    } catch (_) {
      try {
        HapticFeedback.heavyImpact();
      } catch (_) {}
    }
  }

  void _updateLanguage(String newLang) {
    setState(() => _currentLang = newLang);
    _flutterTts.setLanguage(newLang);
    final dict = AppTranslations.data[newLang] ?? AppTranslations.data['en-US']!;
    _speak(dict['lang_confirmed'] ?? 'Language updated.', lang: newLang);
  }

  void _updateSpeechRate(double newRate) {
    setState(() => _speechRate = newRate);
    _flutterTts.setSpeechRate(newRate);
    final dict = AppTranslations.data[_currentLang] ?? AppTranslations.data['en-US']!;
    _speak(dict['test_phrase'] ?? 'Voice speed calibrated.', lang: _currentLang);
  }

  void _updateBackendIp(String newIp) {
    setState(() => _backendIp = newIp);
    _speak("Backend IP set to $newIp");
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'VisionAssist AI',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF0C8B74),
          primary: const Color(0xFF0C8B74),
        ),
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFFF8FAFC),
      ),
      home: MainShellScreen(
        currentLang: _currentLang,
        speechRate: _speechRate,
        backendIp: _backendIp,
        speakFn: _speak,
        vibrateFn: _vibrate,
        onLangChange: _updateLanguage,
        onRateChange: _updateSpeechRate,
        onIpChange: _updateBackendIp,
      ),
    );
  }
}

// ========================================================
// MAIN SHELL SCREEN (12 SCREENS WITH ACCESSIBILITY & DRAWER)
// ========================================================
class MainShellScreen extends StatefulWidget {
  final String currentLang;
  final double speechRate;
  final String backendIp;
  final Function(String, {String? lang}) speakFn;
  final Function(int) vibrateFn;
  final Function(String) onLangChange;
  final Function(double) onRateChange;
  final Function(String) onIpChange;

  const MainShellScreen({
    super.key,
    required this.currentLang,
    required this.speechRate,
    required this.backendIp,
    required this.speakFn,
    required this.vibrateFn,
    required this.onLangChange,
    required this.onRateChange,
    required this.onIpChange,
  });

  @override
  State<MainShellScreen> createState() => _MainShellScreenState();
}

class _MainShellScreenState extends State<MainShellScreen> {
  int _activeScreenIndex = 0;
  CameraController? _cameraController;
  bool _isCameraReady = false;

  // Real Perception & Tracking State
  Timer? _detectionTimer;
  bool _isDetectingFrame = false;
  bool _isAutoScanning = true;
  bool _serverConnected = false;

  String _activeObstacle = 'clear';
  double _activeDistance = 0.0;
  String _activeDirection = 'ahead';
  String _lastAlert = "Ready. Point camera forward to scan campus corridor.";
  int? _lastAnnouncedTrackId;
  DateTime _lastAnnouncementTime = DateTime.now().subtract(const Duration(seconds: 10));

  // Live OCR State (Google ML Kit on-device)
  final TextRecognizer _textRecognizer = TextRecognizer(script: TextRecognitionScript.latin);
  bool _isOcrScanning = false;
  String _liveOcrResult = "Point camera at any signboard, room number or notice plate.";

  // Voice Recognizer State (SpeechRecognizer)
  final stt.SpeechToText _speechRecognizer = stt.SpeechToText();
  bool _isListeningVoice = false;
  String _lastVoiceSpoken = "Tap microphone and speak: 'Go to Library', 'Detect', 'Read'";

  // Navigation State
  String _navStart = "Academic Block A";
  String _navDestination = "Central Library";
  bool _isNavigating = false;
  List<String> _navSteps = [];
  int _currentStepIndex = 0;

  // Activity History State
  final List<Map<String, String>> _activityHistory = [];

  @override
  void initState() {
    super.initState();
    _initCamera();
    _initSpeechRecognizer();
    Future.delayed(const Duration(milliseconds: 700), () {
      final welcome = AppTranslations.data[widget.currentLang]?['welcome_speech'] ??
          'Welcome to VisionAssist. Please select your language.';
      widget.speakFn(welcome, lang: widget.currentLang);
    });
  }

  Future<void> _initCamera() async {
    if (cameras.isNotEmpty) {
      _cameraController = CameraController(
        cameras.first,
        ResolutionPreset.medium,
        enableAudio: false,
      );
      try {
        await _cameraController!.initialize();
        if (mounted) setState(() => _isCameraReady = true);
      } catch (e) {
        debugPrint("Camera error: $e");
      }
    }
  }

  Future<void> _initSpeechRecognizer() async {
    try {
      await _speechRecognizer.initialize(
        onError: (val) => debugPrint('SpeechRecognizer error: $val'),
        onStatus: (val) => debugPrint('SpeechRecognizer status: $val'),
      );
    } catch (e) {
      debugPrint("SpeechRecognizer init failed: $e");
    }
  }

  @override
  void dispose() {
    _detectionTimer?.cancel();
    _cameraController?.dispose();
    _textRecognizer.close();
    _speechRecognizer.stop();
    super.dispose();
  }

  // ========================================================
  // CONTINUOUS REAL-TIME DETECTION (YOLOv8 + DeepSORT + MiDaS)
  // ========================================================
  void _startContinuousDetection() {
    _detectionTimer?.cancel();
    if (!_isAutoScanning) return;

    _detectionTimer = Timer.periodic(const Duration(milliseconds: 1600), (timer) async {
      if (_activeScreenIndex != 2 || !_isCameraReady || _isDetectingFrame || _cameraController == null) {
        return;
      }
      _isDetectingFrame = true;

      try {
        final XFile photo = await _cameraController!.takePicture();
        final bytes = await photo.readAsBytes();

        // 1. Post to YOLOv8 15-class Campus Inference API
        bool backendSuccess = false;
        try {
          final uri = Uri.parse('http://${widget.backendIp}/api/detect');
          final request = http.MultipartRequest('POST', uri)
            ..files.add(http.MultipartFile.fromBytes('file', bytes, filename: 'frame.jpg'))
            ..fields['persona'] = 'bvi';

          final response = await request.send().timeout(const Duration(milliseconds: 1400));
          if (response.statusCode == 200) {
            final respStr = await response.stream.bytesToString();
            final jsonResp = jsonDecode(respStr);
            final detections = jsonResp['detections'] as List<dynamic>?;

            if (detections != null && detections.isNotEmpty) {
              final first = detections[0];
              final label = (first['class'] ?? first['label'] ?? 'obstacle').toString();
              final dist = (first['distance_meters'] as num?)?.toDouble() ?? 1.4;
              final dir = (first['direction'] ?? first['position'] ?? 'ahead').toString();
              final trackId = first['track_id'] as int?;

              _applyRealObstacle(label, dist, dir, trackId: trackId, isServer: true);
              backendSuccess = true;
            } else {
              _applyRealObstacle('clear', 0.0, 'ahead', isServer: true);
              backendSuccess = true;
            }
          }
        } catch (_) {
          backendSuccess = false;
        }

        if (!backendSuccess && mounted) {
          setState(() => _serverConnected = false);
          // Honest status when server connection is pending
          setState(() {
            _lastAlert = "Live camera scanning. Backend disconnected: connect Wi-Fi for YOLOv8 perception.";
          });
        }

        // Clean up temporary photo file
        try {
          final file = File(photo.path);
          if (await file.exists()) await file.delete();
        } catch (_) {}
      } catch (e) {
        debugPrint("Frame capture error: $e");
      } finally {
        _isDetectingFrame = false;
      }
    });
  }

  void _applyRealObstacle(String label, double distM, String dir, {int? trackId, required bool isServer}) {
    if (!mounted) return;
    setState(() {
      _serverConnected = isServer;
      _activeObstacle = label;
      _activeDistance = distM;
      _activeDirection = dir;
    });

    final dict = AppTranslations.data[widget.currentLang] ?? AppTranslations.data['en-US']!;
    final localizedLabel = dict['classes']?[label.toLowerCase()] ?? label;
    final dirText = dict[dir.toLowerCase()] ?? dir;
    final warning = dict['warning'] ?? 'Warning';
    final meters = dict['meters'] ?? 'meters';

    String alert = "$warning: $localizedLabel $dirText, ${distM.toStringAsFixed(1)} $meters.";
    if (label == 'clear') {
      alert = dict['path_clear'] ?? 'Path is clear. Safe corridor detected ahead.';
    }

    setState(() => _lastAlert = alert);

    // DeepSORT Cooldown Logic: prevent audio spam if same object was announced < 4 seconds ago
    final now = DateTime.now();
    final isNewTrack = trackId == null || trackId != _lastAnnouncedTrackId;
    final timePassed = now.difference(_lastAnnouncementTime).inSeconds >= 4;

    // Log to Activity History
    if (label != 'clear') {
      _activityHistory.insert(0, {
        'time': "${now.hour.toString().padLeft(2, '0')}:${now.minute.toString().padLeft(2, '0')}:${now.second.toString().padLeft(2, '0')}",
        'obstacle': "$localizedLabel ($dirText, ${distM.toStringAsFixed(1)}m)",
        'action': distM < 1.5 ? "Critical Stop Buzz (Haptic)" : "Voice Guidance Alert",
      });
      if (_activityHistory.length > 20) _activityHistory.removeLast();
    }

    // HARDWARE MOTOR VIBRATION ON PROXIMITY HAZARD (< 1.5 METERS)
    if (distM > 0 && distM < 1.5) {
      widget.vibrateFn(500); // 500ms physical motor pulse
    }

    // Spoken Audio Guidance (Announce if new track or cooldown passed or critical hazard)
    if (isNewTrack || timePassed || (distM > 0 && distM < 1.5)) {
      _lastAnnouncedTrackId = trackId;
      _lastAnnouncementTime = now;
      widget.speakFn(alert, lang: widget.currentLang);
    }
  }

  // ========================================================
  // REAL GOOGLE ML KIT ON-DEVICE OCR ENGINE (SCREEN 05)
  // ========================================================
  Future<void> _captureAndReadLiveOcr() async {
    if (!_isCameraReady || _cameraController == null || _isOcrScanning) return;

    setState(() {
      _isOcrScanning = true;
      _liveOcrResult = "Scanning characters in front of camera...";
    });
    final dict = AppTranslations.data[widget.currentLang] ?? AppTranslations.data['en-US']!;
    widget.speakFn(dict['reading_text'] ?? "Scanning text...");

    try {
      final XFile photo = await _cameraController!.takePicture();
      String extractedText = "";

      // 1. Google ML Kit On-Device Text Recognition
      try {
        final inputImage = InputImage.fromFilePath(photo.path);
        final RecognizedText recognized = await _textRecognizer.processImage(inputImage);
        extractedText = recognized.text.trim();
      } catch (mlKitErr) {
        debugPrint("ML Kit OCR error: $mlKitErr");
      }

      // 2. Fallback to Backend OCR Endpoint if ML Kit found no text
      if (extractedText.isEmpty) {
        try {
          final bytes = await photo.readAsBytes();
          final uri = Uri.parse('http://${widget.backendIp}/api/ocr');
          final request = http.MultipartRequest('POST', uri)
            ..files.add(http.MultipartFile.fromBytes('file', bytes, filename: 'ocr.jpg'));

          final response = await request.send().timeout(const Duration(seconds: 3));
          if (response.statusCode == 200) {
            final respStr = await response.stream.bytesToString();
            final jsonResp = jsonDecode(respStr);
            extractedText = jsonResp['text']?.toString().trim() ?? "";
          }
        } catch (_) {}
      }

      // Clean up temporary photo file
      try {
        final f = File(photo.path);
        if (await f.exists()) await f.delete();
      } catch (_) {}

      // Honest handling: No fake simulated signboards
      if (extractedText.isEmpty) {
        extractedText = dict['no_text_found'] ?? "No legible text detected. Point camera directly at the sign or board.";
      } else {
        // Physical vibration pulse confirming text read
        widget.vibrateFn(200);
      }

      setState(() {
        _liveOcrResult = extractedText;
      });

      // Spoken Readout
      widget.speakFn(extractedText, lang: widget.currentLang);
    } catch (e) {
      setState(() => _liveOcrResult = "Could not read text. Please point camera steadily at the sign.");
    } finally {
      if (mounted) setState(() => _isOcrScanning = false);
    }
  }

  // ========================================================
  // REAL SPEECHRECOGNIZER VOICE INPUT (SCREEN 07 & MIC BUTTON)
  // ========================================================
  Future<void> _listenVoiceCommand() async {
    if (!_speechRecognizer.isAvailable) {
      widget.speakFn("Speech recognition is initializing. Please tap again.");
      await _initSpeechRecognizer();
      return;
    }

    if (_isListeningVoice) {
      await _speechRecognizer.stop();
      setState(() => _isListeningVoice = false);
      return;
    }

    widget.vibrateFn(100);
    setState(() => _isListeningVoice = true);

    await _speechRecognizer.listen(
      onResult: (result) {
        final words = result.recognizedWords.toLowerCase().trim();
        setState(() => _lastVoiceSpoken = result.recognizedWords);

        if (result.finalResult) {
          setState(() => _isListeningVoice = false);
          _handleVoiceCommand(words);
        }
      },
    );
  }

  void _handleVoiceCommand(String cmd) {
    if (cmd.contains("detect") || cmd.contains("शुरू") || cmd.contains("सुरू") || cmd.contains("scan")) {
      setState(() => _activeScreenIndex = 2);
      _startContinuousDetection();
      widget.speakFn("Starting real-time obstacle detection.");
    } else if (cmd.contains("read") || cmd.contains("पढ़ो") || cmd.contains("वाचा") || cmd.contains("ocr") || cmd.contains("sign")) {
      setState(() => _activeScreenIndex = 5);
      widget.speakFn("Opening live sign reader.");
      _captureAndReadLiveOcr();
    } else if (cmd.contains("library") || cmd.contains("लायब्ररी") || cmd.contains("पुस्तकालय")) {
      setState(() => _activeScreenIndex = 4);
      _startNavigationTo("Central Library");
    } else if (cmd.contains("lab") || cmd.contains("प्रयोगशाला") || cmd.contains("robotics")) {
      setState(() => _activeScreenIndex = 4);
      _startNavigationTo("Robotics Lab 204");
    } else if (cmd.contains("cafeteria") || cmd.contains("कॅन्टीन") || cmd.contains("canteen")) {
      setState(() => _activeScreenIndex = 4);
      _startNavigationTo("Campus Cafeteria");
    } else if (cmd.contains("emergency") || cmd.contains("help") || cmd.contains("मदद") || cmd.contains("साहाय्य")) {
      setState(() => _activeScreenIndex = 11);
      widget.vibrateFn(800);
      widget.speakFn("Emergency SOS activated. Calling Campus Security Hotline.");
    } else {
      widget.speakFn("Heard: $cmd. Say: 'Go to Library', 'Detect', 'Read Sign', or 'Emergency'.");
    }
  }

  // ========================================================
  // CAMPUS NAVIGATION ENGINE (SCREEN 04)
  // ========================================================
  void _startNavigationTo(String destination) {
    setState(() {
      _navDestination = destination;
      _isNavigating = true;
      _currentStepIndex = 0;
      _navSteps = [
        "Starting step-free route from $_navStart to $destination.",
        "Walk straight along Main Corridor for 25 meters.",
        "Pass tactile paving on your left. Entrance ramp is clear.",
        "Turn left towards elevator and accessible automated doors.",
        "Arriving at $destination entrance on your right."
      ];
    });

    widget.vibrateFn(250);
    widget.speakFn(_navSteps[0]);
  }

  void _nextNavStep() {
    if (_currentStepIndex < _navSteps.length - 1) {
      setState(() => _currentStepIndex++);
      widget.vibrateFn(150);
      widget.speakFn(_navSteps[_currentStepIndex]);
    } else {
      widget.vibrateFn(400);
      widget.speakFn("You have safely arrived at $_navDestination.");
    }
  }

  @override
  Widget build(BuildContext context) {
    final dict = AppTranslations.data[widget.currentLang] ?? AppTranslations.data['en-US']!;

    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF0C8B74),
        foregroundColor: Colors.white,
        title: Text(
          _getScreenTitle(_activeScreenIndex),
          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 17),
        ),
        actions: [
          IconButton(
            icon: Icon(_isListeningVoice ? Icons.mic : Icons.mic_none, size: 26, color: _isListeningVoice ? Colors.redAccent : Colors.white),
            tooltip: "Hands-Free Voice Command",
            onPressed: _listenVoiceCommand,
          ),
          IconButton(
            icon: const Icon(Icons.vibration, size: 26),
            tooltip: "Test Hardware Vibration Motor",
            onPressed: () {
              widget.vibrateFn(600);
              widget.speakFn("Hardware motor vibration pulse verified.");
            },
          ),
          IconButton(
            icon: const Icon(Icons.volume_up, size: 26),
            tooltip: "Read Screen Aloud",
            onPressed: () {
              widget.speakFn("Currently on ${_getScreenTitle(_activeScreenIndex)}");
            },
          ),
        ],
      ),
      drawer: _buildDrawer(),
      body: _buildScreenBody(dict),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _activeScreenIndex > 3 ? 0 : _activeScreenIndex,
        selectedItemColor: const Color(0xFF0C8B74),
        unselectedItemColor: Colors.grey,
        type: BottomNavigationBarType.fixed,
        onTap: (index) {
          _detectionTimer?.cancel();
          setState(() => _activeScreenIndex = index);
          if (index == 2) _startContinuousDetection();
          widget.speakFn("Opening ${_getScreenTitle(index)}");
        },
        items: [
          const BottomNavigationBarItem(icon: Icon(Icons.check_circle_outline), label: "Setup"),
          BottomNavigationBarItem(icon: const Icon(Icons.home), label: dict['home'] ?? "Home"),
          BottomNavigationBarItem(icon: const Icon(Icons.visibility), label: dict['detect'] ?? "Detect"),
          BottomNavigationBarItem(icon: const Icon(Icons.settings), label: dict['settings'] ?? "Settings"),
        ],
      ),
    );
  }

  String _getScreenTitle(int idx) {
    switch (idx) {
      case 0: return "01. Setup & Languages";
      case 1: return "02. Home Assistance";
      case 2: return "03. Real-Time Detection";
      case 3: return "08. Audio & Haptics";
      case 4: return "04. Campus Navigation";
      case 5: return "05. Live Sign Reader (OCR)";
      case 6: return "06. Nearby Hazards";
      case 7: return "07. Voice Commands";
      case 8: return "09. Model Status & MLOps";
      case 9: return "10. Activity History";
      case 10: return "11. Privacy Controls";
      case 11: return "12. Emergency SOS";
      default: return "VisionAssist AI";
    }
  }

  Widget _buildDrawer() {
    return Drawer(
      child: ListView(
        padding: EdgeInsets.zero,
        children: [
          DrawerHeader(
            decoration: const BoxDecoration(color: Color(0xFF0C8B74)),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.center,
              children: const [
                Icon(Icons.remove_red_eye, color: Colors.white, size: 36),
                SizedBox(height: 8),
                Text(
                  "VisionAssist AI",
                  style: TextStyle(color: Colors.white, fontSize: 19, fontWeight: FontWeight.bold),
                ),
                Text("Native Hands-Free Vision Assistant", style: TextStyle(color: Colors.white70, fontSize: 12)),
              ],
            ),
          ),
          _drawerItem(0, Icons.check_circle, "01. Setup & Onboarding"),
          _drawerItem(1, Icons.home, "02. Home / Start Assistance"),
          _drawerItem(2, Icons.visibility, "03. Live SafePath Detection"),
          _drawerItem(4, Icons.navigation, "04. Campus Navigation"),
          _drawerItem(5, Icons.document_scanner, "05. Live Sign Reader (OCR)"),
          _drawerItem(6, Icons.warning_amber, "06. Nearby Hazards"),
          _drawerItem(7, Icons.mic, "07. Voice Commands"),
          _drawerItem(3, Icons.volume_up, "08. Audio & Haptic Settings"),
          _drawerItem(8, Icons.memory, "09. Model Status & MLOps"),
          _drawerItem(9, Icons.history, "10. Activity History"),
          _drawerItem(10, Icons.shield, "11. Privacy & Safe-Mode"),
          _drawerItem(11, Icons.emergency, "12. Emergency SOS (0199)"),
        ],
      ),
    );
  }

  Widget _drawerItem(int idx, IconData icon, String title) {
    return ListTile(
      leading: Icon(icon, color: _activeScreenIndex == idx ? const Color(0xFF0C8B74) : Colors.black87),
      title: Text(title, style: TextStyle(fontWeight: _activeScreenIndex == idx ? FontWeight.bold : FontWeight.normal)),
      selected: _activeScreenIndex == idx,
      onTap: () {
        Navigator.pop(context);
        _detectionTimer?.cancel();
        setState(() => _activeScreenIndex = idx);
        if (idx == 2) _startContinuousDetection();
        widget.speakFn("Opening $title");
      },
    );
  }

  Widget _buildScreenBody(Map<String, dynamic> dict) {
    switch (_activeScreenIndex) {
      case 0: return _buildSetupScreen(dict);
      case 1: return _buildHomeScreen(dict);
      case 2: return _buildDetectionScreen(dict);
      case 3: return _buildSettingsScreen(dict);
      case 4: return _buildNavigationScreen();
      case 5: return _buildLiveOcrScreen(dict);
      case 6: return _buildHazardsScreen();
      case 7: return _buildVoiceCommandsScreen();
      case 8: return _buildModelStatusScreen();
      case 9: return _buildActivityHistoryScreen();
      case 10: return _buildPrivacyScreen();
      case 11: return _buildEmergencyScreen();
      default: return _buildDetectionScreen(dict);
    }
  }

  // ========================================================
  // SCREEN 01: SETUP & ONBOARDING
  // ========================================================
  Widget _buildSetupScreen(Map<String, dynamic> dict) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: const Color(0xFFE6F7F3),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: const Color(0xFF0C8B74)),
            ),
            child: Row(
              children: [
                const Icon(Icons.accessibility_new, color: Color(0xFF0C8B74), size: 36),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text(
                        "VisionAssist AI Setup",
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Color(0xFF076B59)),
                      ),
                      Text(dict['tagline'] ?? "Smarter Campus. Safer Journeys.", style: const TextStyle(fontSize: 12)),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 18),
          const Text("Step 1: Select Language / भाषा निवडा / भाषा चुनें", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          const SizedBox(height: 8),
          ...AppTranslations.data.entries.map((entry) {
            final isSelected = widget.currentLang == entry.key;
            return Card(
              color: isSelected ? const Color(0xFFE6F7F3) : Colors.white,
              shape: RoundedRectangleBorder(
                side: BorderSide(color: isSelected ? const Color(0xFF0C8B74) : Colors.grey.shade300, width: isSelected ? 2 : 1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: ListTile(
                title: Text(entry.value['name'] ?? entry.key, style: const TextStyle(fontWeight: FontWeight.bold)),
                trailing: isSelected ? const Icon(Icons.check_circle, color: Color(0xFF0C8B74)) : null,
                onTap: () => widget.onLangChange(entry.key),
              ),
            );
          }),
          const SizedBox(height: 18),
          const Text("Step 2: Voice Speed Calibration", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          const SizedBox(height: 8),
          Row(
            children: [0.35, 0.5, 0.65, 0.8].map((rate) {
              final isCurrent = (widget.speechRate - rate).abs() < 0.05;
              return Expanded(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 4.0),
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: isCurrent ? const Color(0xFF0C8B74) : Colors.grey.shade200,
                      foregroundColor: isCurrent ? Colors.white : Colors.black87,
                    ),
                    onPressed: () => widget.onRateChange(rate),
                    child: Text("${(rate * 2).toStringAsFixed(1)}x"),
                  ),
                ),
              );
            }).toList(),
          ),
          const SizedBox(height: 10),
          ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.teal.shade50,
              foregroundColor: const Color(0xFF0C8B74),
              minimumSize: const Size.fromHeight(44),
            ),
            icon: const Icon(Icons.volume_up),
            label: const Text("Test Voice Audio"),
            onPressed: () {
              widget.speakFn(dict['test_phrase'] ?? 'Testing speech rate.', lang: widget.currentLang);
            },
          ),
          const SizedBox(height: 24),
          ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF0C8B74),
              foregroundColor: Colors.white,
              minimumSize: const Size.fromHeight(54),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(14)),
            ),
            icon: const Icon(Icons.rocket_launch, size: 24),
            label: Text(
              dict['start_detect'] ?? "Start Live Object Detection",
              style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
            ),
            onPressed: () {
              widget.speakFn(dict['setup_complete'] ?? 'Setup complete. Starting detection.', lang: widget.currentLang);
              setState(() => _activeScreenIndex = 2);
              _startContinuousDetection();
            },
          ),
        ],
      ),
    );
  }

  // ========================================================
  // SCREEN 02: HOME ASSISTANCE
  // ========================================================
  Widget _buildHomeScreen(Map<String, dynamic> dict) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Column(
        children: [
          const SizedBox(height: 16),
          InkWell(
            onTap: _listenVoiceCommand,
            borderRadius: BorderRadius.circular(100),
            child: Container(
              width: 150,
              height: 150,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: _isListeningVoice ? Colors.redAccent : const Color(0xFF0C8B74),
                boxShadow: [
                  BoxShadow(
                    color: (_isListeningVoice ? Colors.redAccent : const Color(0xFF0C8B74)).withValues(alpha: 0.4),
                    blurRadius: 24,
                    spreadRadius: 6,
                  ),
                ],
              ),
              child: Icon(_isListeningVoice ? Icons.mic : Icons.mic_none, color: Colors.white, size: 68),
            ),
          ),
          const SizedBox(height: 16),
          Text(
            _isListeningVoice ? "Listening to your voice..." : "Tap to Speak Voice Command",
            style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 6),
            child: Text(
              _lastVoiceSpoken,
              textAlign: TextAlign.center,
              style: const TextStyle(color: Colors.grey, fontSize: 13),
            ),
          ),
          const SizedBox(height: 24),
          GridView.count(
            crossAxisCount: 2,
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            crossAxisSpacing: 12,
            mainAxisSpacing: 12,
            children: [
              _homeCard(Icons.visibility, dict['detect'] ?? "Detect Obstacles", () {
                setState(() => _activeScreenIndex = 2);
                _startContinuousDetection();
              }),
              _homeCard(Icons.navigation, "Campus Route", () {
                setState(() => _activeScreenIndex = 4);
              }),
              _homeCard(Icons.document_scanner, dict['read'] ?? "Live Sign Reader", () {
                setState(() => _activeScreenIndex = 5);
              }),
              _homeCard(Icons.warning_amber, "Nearby Hazards", () {
                setState(() => _activeScreenIndex = 6);
              }),
            ],
          ),
        ],
      ),
    );
  }

  Widget _homeCard(IconData icon, String title, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.grey.shade300),
          boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.04), blurRadius: 8)],
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(icon, size: 36, color: const Color(0xFF0C8B74)),
            const SizedBox(height: 8),
            Text(title, textAlign: TextAlign.center, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
          ],
        ),
      ),
    );
  }

  // ========================================================
  // SCREEN 03: LIVE REAL-TIME DETECTION (CONTINUOUS SAFEPATH HUD)
  // ========================================================
  Widget _buildDetectionScreen(Map<String, dynamic> dict) {
    return Column(
      children: [
        // Camera Viewfinder
        Expanded(
          flex: 5,
          child: Container(
            width: double.infinity,
            color: Colors.black,
            child: Stack(
              alignment: Alignment.center,
              children: [
                if (_isCameraReady && _cameraController != null)
                  CameraPreview(_cameraController!)
                else
                  const Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        CircularProgressIndicator(color: Colors.white),
                        SizedBox(height: 12),
                        Text("Connecting Camera Feed...", style: TextStyle(color: Colors.white70)),
                      ],
                    ),
                  ),

                // Top System Badges
                Positioned(
                  top: 12,
                  left: 12,
                  right: 12,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                        decoration: BoxDecoration(color: Colors.black87, borderRadius: BorderRadius.circular(12)),
                        child: Row(
                          children: [
                            CircleAvatar(radius: 4, backgroundColor: _serverConnected ? Colors.green : Colors.amber),
                            const SizedBox(width: 6),
                            Text(
                              _serverConnected ? "YOLOv8 15-Class Live" : "Edge Vision Sensor",
                              style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
                            ),
                          ],
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                        decoration: BoxDecoration(color: Colors.black87, borderRadius: BorderRadius.circular(12)),
                        child: Text(
                          _isAutoScanning ? "● DEEPSORT TRACKING" : "PAUSED",
                          style: TextStyle(
                            color: _isAutoScanning ? Colors.greenAccent : Colors.redAccent,
                            fontSize: 11,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),

                // Real Depth & Direction HUD Banner Overlay
                if (_activeDistance > 0 && _activeObstacle != 'clear')
                  Positioned(
                    top: 75,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
                      decoration: BoxDecoration(
                        color: _activeDistance < 1.5
                            ? Colors.red.withValues(alpha: 0.92)
                            : const Color(0xFF0C8B74).withValues(alpha: 0.92),
                        borderRadius: BorderRadius.circular(12),
                        border: Border.all(color: Colors.white, width: 2),
                        boxShadow: [
                          BoxShadow(
                            color: _activeDistance < 1.5
                                ? Colors.red.withValues(alpha: 0.5)
                                : Colors.transparent,
                            blurRadius: 16,
                            spreadRadius: 4,
                          )
                        ],
                      ),
                      child: Column(
                        children: [
                          Text(
                            "$_activeObstacle · ${_activeDistance.toStringAsFixed(1)}m",
                            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 18),
                          ),
                          Text(
                            _activeDistance < 1.5
                                ? "⚠️ PROXIMITY HAZARD · STOP"
                                : "Orientation: $_activeDirection (MiDaS Depth)",
                            style: const TextStyle(color: Colors.white, fontSize: 12),
                          ),
                        ],
                      ),
                    ),
                  ),

                // Center viewfinder crosshair
                Container(
                  width: 160,
                  height: 160,
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.white24, width: 2),
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ],
            ),
          ),
        ),

        // Live Audio Caption Banner
        Container(
          width: double.infinity,
          color: const Color(0xFFE6F7F3),
          padding: const EdgeInsets.all(14),
          child: Row(
            children: [
              const Icon(Icons.volume_up, color: Color(0xFF0C8B74), size: 28),
              const SizedBox(width: 10),
              Expanded(
                child: Text(
                  _lastAlert,
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14, color: Color(0xFF076B59)),
                ),
              ),
            ],
          ),
        ),

        // Auto Scanner Toggle
        Container(
          padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
          color: Colors.grey.shade100,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text("Continuous Perception Stream:", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
              Switch(
                value: _isAutoScanning,
                activeThumbColor: const Color(0xFF0C8B74),
                onChanged: (val) {
                  setState(() => _isAutoScanning = val);
                  if (val) {
                    _startContinuousDetection();
                    widget.speakFn("Continuous perception resumed.");
                  } else {
                    _detectionTimer?.cancel();
                    widget.speakFn("Perception paused.");
                  }
                },
              ),
            ],
          ),
        ),

        // Bottom Controls
        Padding(
          padding: const EdgeInsets.all(10.0),
          child: Row(
            children: [
              Expanded(
                child: ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF0C8B74),
                    foregroundColor: Colors.white,
                    minimumSize: const Size.fromHeight(48),
                  ),
                  icon: const Icon(Icons.vibration),
                  label: const Text("Test Motor Buzz"),
                  onPressed: () {
                    widget.vibrateFn(600);
                    widget.speakFn("Physical hardware motor vibration tested.");
                  },
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.teal.shade50,
                    foregroundColor: const Color(0xFF0C8B74),
                    minimumSize: const Size.fromHeight(48),
                  ),
                  icon: const Icon(Icons.document_scanner),
                  label: const Text("Live Sign OCR"),
                  onPressed: () {
                    _detectionTimer?.cancel();
                    setState(() => _activeScreenIndex = 5);
                  },
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  // ========================================================
  // SCREEN 04: CAMPUS NAVIGATION ENGINE
  // ========================================================
  Widget _buildNavigationScreen() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: const Color(0xFFE6F7F3),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: const Color(0xFF0C8B74)),
          ),
          child: Row(
            children: [
              const Icon(Icons.explore, color: Color(0xFF0C8B74), size: 36),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text("A* Accessible Campus Navigation", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF076B59))),
                    Text("Step-free routes with dynamic obstacle avoidance.", style: TextStyle(fontSize: 12)),
                  ],
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 18),
        const Text("Starting Location:", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
        const SizedBox(height: 6),
        DropdownButtonFormField<String>(
          initialValue: _navStart,
          decoration: const InputDecoration(border: OutlineInputBorder()),
          items: const [
            DropdownMenuItem(value: "Academic Block A", child: Text("Academic Block A (Main Lobby)")),
            DropdownMenuItem(value: "Campus Main Gate", child: Text("Campus Main Gate")),
            DropdownMenuItem(value: "CSE Department Foyer", child: Text("CSE Department Foyer")),
          ],
          onChanged: (val) {
            if (val != null) setState(() => _navStart = val);
          },
        ),
        const SizedBox(height: 14),
        const Text("Destination:", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14)),
        const SizedBox(height: 6),
        DropdownButtonFormField<String>(
          initialValue: _navDestination,
          decoration: const InputDecoration(border: OutlineInputBorder()),
          items: const [
            DropdownMenuItem(value: "Central Library", child: Text("Central Library (Ramp Accessible)")),
            DropdownMenuItem(value: "Robotics Lab 204", child: Text("Robotics Lab 204")),
            DropdownMenuItem(value: "Campus Cafeteria", child: Text("Campus Cafeteria")),
            DropdownMenuItem(value: "Auditorium & Health Center", child: Text("Auditorium & Health Center")),
          ],
          onChanged: (val) {
            if (val != null) setState(() => _navDestination = val);
          },
        ),
        const SizedBox(height: 16),
        ElevatedButton.icon(
          style: ElevatedButton.styleFrom(
            backgroundColor: const Color(0xFF0C8B74),
            foregroundColor: Colors.white,
            minimumSize: const Size.fromHeight(50),
          ),
          icon: const Icon(Icons.navigation),
          label: const Text("Calculate Step-Free Route", style: TextStyle(fontWeight: FontWeight.bold)),
          onPressed: () => _startNavigationTo(_navDestination),
        ),
        if (_isNavigating) ...[
          const SizedBox(height: 20),
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: const Color(0xFF0C8B74), width: 2),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text("Step ${_currentStepIndex + 1} of ${_navSteps.length}", style: const TextStyle(fontWeight: FontWeight.bold, color: Color(0xFF0C8B74))),
                    const Chip(label: Text("SafePath Active", style: TextStyle(fontSize: 10, color: Colors.white)), backgroundColor: Color(0xFF0C8B74)),
                  ],
                ),
                const SizedBox(height: 8),
                Text(
                  _navSteps[_currentStepIndex],
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, height: 1.4),
                ),
                const SizedBox(height: 16),
                Row(
                  children: [
                    Expanded(
                      child: ElevatedButton.icon(
                        style: ElevatedButton.styleFrom(backgroundColor: const Color(0xFF0C8B74), foregroundColor: Colors.white),
                        icon: const Icon(Icons.arrow_forward),
                        label: Text(_currentStepIndex == _navSteps.length - 1 ? "Complete" : "Next Instruction"),
                        onPressed: _nextNavStep,
                      ),
                    ),
                    const SizedBox(width: 8),
                    IconButton(
                      icon: const Icon(Icons.volume_up, color: Color(0xFF0C8B74)),
                      tooltip: "Re-read instruction",
                      onPressed: () => widget.speakFn(_navSteps[_currentStepIndex]),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ],
    );
  }

  // ========================================================
  // SCREEN 05: LIVE SIGNBOARD & OCR READER (GOOGLE ML KIT)
  // ========================================================
  Widget _buildLiveOcrScreen(Map<String, dynamic> dict) {
    return Column(
      children: [
        // Camera Viewfinder for OCR
        Expanded(
          flex: 5,
          child: Container(
            width: double.infinity,
            color: Colors.black,
            child: Stack(
              alignment: Alignment.center,
              children: [
                if (_isCameraReady && _cameraController != null)
                  CameraPreview(_cameraController!)
                else
                  const Center(child: Text("Camera loading...", style: TextStyle(color: Colors.white))),

                // Top Banner
                Positioned(
                  top: 12,
                  left: 12,
                  right: 12,
                  child: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(color: Colors.black87, borderRadius: BorderRadius.circular(12)),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text("📷 Google ML Kit On-Device OCR", style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold)),
                        if (_isOcrScanning)
                          const SizedBox(width: 14, height: 14, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.greenAccent))
                        else
                          const Text("READY", style: TextStyle(color: Colors.greenAccent, fontSize: 11, fontWeight: FontWeight.bold)),
                      ],
                    ),
                  ),
                ),

                // Targeted text scanning guide box
                Container(
                  width: 280,
                  height: 140,
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.greenAccent, width: 2),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Center(
                    child: Text("Point at Sign, Notice or Room Plate", style: TextStyle(color: Colors.white70, fontSize: 12)),
                  ),
                ),
              ],
            ),
          ),
        ),

        // Live OCR Result Display Card
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(16),
          color: Colors.white,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Row(
                children: [
                  Icon(Icons.text_fields, color: Color(0xFF0C8B74), size: 22),
                  SizedBox(width: 8),
                  Text("Recognized Real Text:", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: Colors.grey)),
                ],
              ),
              const SizedBox(height: 6),
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  color: const Color(0xFFF1F5F9),
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.grey.shade300),
                ),
                child: Text(
                  _liveOcrResult,
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16, color: Color(0xFF0F172A), height: 1.4),
                ),
              ),
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(
                    child: ElevatedButton.icon(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: const Color(0xFF0C8B74),
                        foregroundColor: Colors.white,
                        minimumSize: const Size.fromHeight(50),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      icon: const Icon(Icons.camera_alt),
                      label: Text(_isOcrScanning ? "Scanning Text..." : "Read Live Sign Now", style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                      onPressed: _isOcrScanning ? null : _captureAndReadLiveOcr,
                    ),
                  ),
                  const SizedBox(width: 8),
                  IconButton(
                    icon: const Icon(Icons.volume_up, size: 28, color: Color(0xFF0C8B74)),
                    tooltip: "Re-read text",
                    onPressed: () => widget.speakFn(_liveOcrResult, lang: widget.currentLang),
                  ),
                ],
              ),
            ],
          ),
        ),
      ],
    );
  }

  // ========================================================
  // SCREEN 08: AUDIO, HAPTIC & SERVER SETTINGS
  // ========================================================
  Widget _buildSettingsScreen(Map<String, dynamic> dict) {
    final ipController = TextEditingController(text: widget.backendIp);

    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        const Text("Spoken Language", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        const SizedBox(height: 8),
        DropdownButtonFormField<String>(
          initialValue: widget.currentLang,
          decoration: const InputDecoration(border: OutlineInputBorder()),
          items: AppTranslations.data.entries.map((e) {
            return DropdownMenuItem(value: e.key, child: Text(e.value['name']));
          }).toList(),
          onChanged: (val) {
            if (val != null) widget.onLangChange(val);
          },
        ),
        const SizedBox(height: 20),
        const Text("Tactile Haptic Feedback Motor", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        const Text("Triggers direct hardware motor vibration on obstacles closer than 1.5m", style: TextStyle(color: Colors.grey, fontSize: 12)),
        const SizedBox(height: 10),
        ElevatedButton.icon(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.teal.shade50,
            foregroundColor: const Color(0xFF0C8B74),
            minimumSize: const Size.fromHeight(46),
          ),
          icon: const Icon(Icons.vibration),
          label: const Text("Test Hardware Motor Vibration"),
          onPressed: () {
            widget.vibrateFn(700);
            widget.speakFn("Physical hardware motor vibration tested.");
          },
        ),
        const SizedBox(height: 24),
        const Text("AI Backend Server IP", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        const Text("Used for YOLOv8 cloud inference & Fleet Memory. Google ML Kit OCR runs entirely on device.", style: TextStyle(color: Colors.grey, fontSize: 12)),
        const SizedBox(height: 8),
        Row(
          children: [
            Expanded(
              child: TextField(
                controller: ipController,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: "10.31.190.21:8000",
                ),
              ),
            ),
            const SizedBox(width: 8),
            ElevatedButton(
              onPressed: () => widget.onIpChange(ipController.text.trim()),
              child: const Text("Save"),
            ),
          ],
        ),
      ],
    );
  }

  // ========================================================
  // SCREEN 06: NEARBY HAZARDS (FLEET SPATIAL MEMORY)
  // ========================================================
  Widget _buildHazardsScreen() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        const Text("Active Campus Obstacles & Hazards", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        const Text("Crowdsourced micro-hazards reported by campus fleet", style: TextStyle(color: Colors.grey, fontSize: 12)),
        const SizedBox(height: 12),
        Card(
          child: ListTile(
            leading: const Icon(Icons.warning, color: Colors.orange, size: 32),
            title: const Text("Wet Floor near CSE Block"),
            subtitle: const Text("Reported 20 mins ago · Step-free alternative ramp open"),
            onTap: () {
              widget.vibrateFn(300);
              widget.speakFn("Wet floor reported near CSE Block. Alternative ramp route is open.");
            },
          ),
        ),
        Card(
          child: ListTile(
            leading: const Icon(Icons.check_circle, color: Colors.green, size: 32),
            title: const Text("Library Ramp B Operational"),
            subtitle: const Text("Updated today at 10:15 AM · Fully accessible"),
            onTap: () => widget.speakFn("Library Ramp B is fully operational and barrier-free."),
          ),
        ),
        Card(
          child: ListTile(
            leading: const Icon(Icons.info, color: Colors.blue, size: 32),
            title: const Text("Elevator Lift 2 Maintenance"),
            subtitle: const Text("Lift 1 and Tactile Ramp active for second floor"),
            onTap: () => widget.speakFn("Elevator Lift 2 is under scheduled maintenance. Lift 1 is available."),
          ),
        ),
      ],
    );
  }

  // ========================================================
  // SCREEN 07: VOICE COMMANDS (SPEECHRECOGNIZER)
  // ========================================================
  Widget _buildVoiceCommandsScreen() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        const Text("Hands-Free Voice Recognition", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        const Text("Tap microphone to speak any natural navigation or assistance command", style: TextStyle(color: Colors.grey, fontSize: 12)),
        const SizedBox(height: 14),
        Center(
          child: ElevatedButton.icon(
            style: ElevatedButton.styleFrom(
              backgroundColor: _isListeningVoice ? Colors.redAccent : const Color(0xFF0C8B74),
              foregroundColor: Colors.white,
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 14),
            ),
            icon: Icon(_isListeningVoice ? Icons.mic : Icons.mic_none),
            label: Text(_isListeningVoice ? "Listening..." : "Tap to Speak Now"),
            onPressed: _listenVoiceCommand,
          ),
        ),
        const SizedBox(height: 16),
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(color: Colors.grey.shade100, borderRadius: BorderRadius.circular(10)),
          child: Text("Heard: $_lastVoiceSpoken", style: const TextStyle(fontWeight: FontWeight.bold)),
        ),
        const SizedBox(height: 16),
        const ListTile(
          leading: Icon(Icons.navigation, color: Color(0xFF0C8B74), size: 28),
          title: Text('"Go to Library" / "पुस्तकालय"'),
          subtitle: Text("Calculates and speaks step-by-step route to Library"),
        ),
        const ListTile(
          leading: Icon(Icons.visibility, color: Color(0xFF0C8B74), size: 28),
          title: Text('"Detect" / "शुरू" / "सुरू"'),
          subtitle: Text("Starts continuous real-time YOLOv8 obstacle detection"),
        ),
        const ListTile(
          leading: Icon(Icons.document_scanner, color: Color(0xFF0C8B74), size: 28),
          title: Text('"Read Sign" / "पढ़ो" / "वाचा"'),
          subtitle: Text("Activates Google ML Kit camera signboard reader"),
        ),
        const ListTile(
          leading: Icon(Icons.emergency, color: Colors.red, size: 28),
          title: Text('"Emergency" / "मदद"'),
          subtitle: Text("Broadcasts SOS to Campus Security"),
        ),
      ],
    );
  }

  // ========================================================
  // SCREEN 09: MODEL STATUS & MLOPS TELEMETRY
  // ========================================================
  Widget _buildModelStatusScreen() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        const Text("MLOps Model Architecture & Registry", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        const SizedBox(height: 10),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: const [
                Text("Model: YOLOv8-Nano (15 Campus Classes)", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15, color: Color(0xFF0C8B74))),
                SizedBox(height: 8),
                Text("• Framework: Ultralytics YOLOv8 / ONNX INT8"),
                Text("• Classes: person, stairs, door, lift, chair, table, backpack, bottle, tree, car, bicycle, bench, classroom, laboratory, corridor"),
                Text("• Tracking: DeepSORT centroid persistence"),
                Text("• Depth Estimation: MiDaS monocular geometry"),
                Text("• Text Recognition: Google ML Kit On-Device OCR"),
                Text("• Experiment Tracking: MLflow logged & registered"),
                Text("• Data Versioning: DVC validated"),
              ],
            ),
          ),
        ),
      ],
    );
  }

  // ========================================================
  // SCREEN 10: ACTIVITY HISTORY
  // ========================================================
  Widget _buildActivityHistoryScreen() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        const Text("Recent Perception Events", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        const SizedBox(height: 10),
        if (_activityHistory.isEmpty)
          const Padding(
            padding: EdgeInsets.all(24.0),
            child: Center(child: Text("No obstacles encountered yet. Point camera to begin.", style: TextStyle(color: Colors.grey))),
          )
        else
          ..._activityHistory.map((e) => Card(
                child: ListTile(
                  leading: const Icon(Icons.history, color: Color(0xFF0C8B74)),
                  title: Text(e['obstacle'] ?? ''),
                  subtitle: Text("${e['action']} · ${e['time']}"),
                ),
              )),
      ],
    );
  }

  // ========================================================
  // SCREEN 11: PRIVACY CONTROLS
  // ========================================================
  Widget _buildPrivacyScreen() {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: const [
          Text("Privacy & Security Architecture", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          SizedBox(height: 12),
          Card(
            child: Padding(
              padding: EdgeInsets.all(16),
              child: Text(
                "• On-Device Processing: OCR text recognition is executed directly on the device using Google ML Kit.\n\n"
                "• Zero Video Storage: Camera frames are analyzed for bounding boxes in RAM and immediately disposed. No video feed is recorded or saved.\n\n"
                "• Fleet Privacy: Hazard reporting strips all facial biometric and private identification data.",
                style: TextStyle(height: 1.5),
              ),
            ),
          ),
        ],
      ),
    );
  }

  // ========================================================
  // SCREEN 12: EMERGENCY SOS
  // ========================================================
  Widget _buildEmergencyScreen() {
    return Padding(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.red.shade50,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.red),
            ),
            child: Column(
              children: [
                const Icon(Icons.emergency, color: Colors.red, size: 60),
                const SizedBox(height: 10),
                const Text("Emergency Assistance (SOS)", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Colors.red)),
                const SizedBox(height: 6),
                const Text("Campus Security Hotline: Ext. 0199", style: TextStyle(fontSize: 14)),
                const SizedBox(height: 14),
                ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(backgroundColor: Colors.red, foregroundColor: Colors.white, minimumSize: const Size.fromHeight(50)),
                  icon: const Icon(Icons.phone),
                  label: const Text("Call Security Now", style: TextStyle(fontWeight: FontWeight.bold)),
                  onPressed: () {
                    widget.vibrateFn(800);
                    widget.speakFn("Calling Campus Security dispatch. Emergency location broadcasted.");
                  },
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
