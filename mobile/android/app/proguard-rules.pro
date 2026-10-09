# Flutter specific ProGuard rules
-keep class io.flutter.** { *; }
-keep class io.flutter.plugins.**  { *; }

# Keep Gson/JSON serialization
-keepattributes Signature
-keepattributes *Annotation*

# Dio HTTP client
-keep class com.squareup.okhttp3.** { *; }
-keep interface com.squareup.okhttp3.** { *; }
-dontwarn com.squareup.okhttp3.**
-dontwarn okio.**
