import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const { name, phone, message } = await request.json();

    const botToken = process.env.TELEGRAM_BOT_TOKEN;
    const chatId = process.env.TELEGRAM_CHAT_ID;

    if (!botToken || !chatId) {
      console.warn("Telegram bot token or chat ID is missing. Logging support request instead:");
      console.log(`Support Request -> Name: ${name}, Phone: ${phone}, Message: ${message}`);
      // Simulate success even if telegram isn't configured yet
      return NextResponse.json({ success: true }, { status: 200 });
    }

    const text = `🚨 *Yangi murojaat (Rasta B2B)*\n\n👤 *Ism/Tashkilot:* ${name}\n📱 *Telefon:* ${phone}\n💬 *Xabar:* ${message}`;

    const telegramRes = await fetch(`https://api.telegram.org/bot${botToken}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: chatId,
        text: text,
        parse_mode: 'Markdown',
      }),
    });

    if (!telegramRes.ok) {
      console.error("Telegram API Error:", await telegramRes.text());
      return NextResponse.json({ error: 'Failed to send to Telegram' }, { status: 500 });
    }

    return NextResponse.json({ success: true }, { status: 200 });
  } catch (error) {
    console.error("Support Route Error:", error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
