// Konnect AI website chat: proxies the on-page chat widget to the Claude API.
// Needs ANTHROPIC_API_KEY set in Netlify: Project configuration -> Environment variables.
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // reads ANTHROPIC_API_KEY from the environment

const SYSTEM = `You are the website assistant for Konnect AI. You chat with visitors on konnectai.org.

About Konnect AI:
- Positioning: Konnect AI helps businesses land more clients, save time and automate tasks. Tagline: "We can build anything."
- Builds fully custom AI automation systems for businesses: AI chat and voice agents, lead capture and instant follow-up, document and data processing, workflow automation, reporting dashboards, and fully custom builds. Systems connect to the tools a business already uses (CRMs, email, phones, calendars, spreadsheets, industry software).
- Also builds mobile-first websites for local businesses: tap-to-call, lead forms that email the owner, online booking, Google-ready setup, with hosting and updates handled.
- Process: 1) free discovery call, 2) a written plan and price the client approves, 3) build with regular demos, tested on real cases, 4) launch, training and ongoing support.
- The client owns the system or website. Clients work directly with the people building it.
- Founder: Tristan Karim. Email tristan@getkonnectai.com, phone (248) 938-1582.
- Book a free build call: https://calendar.app.google/ZGPwJmMpcz3yWbkt5

How to reply:
- Keep replies short: two to four sentences, plain text, no markdown headings or tables.
- Be friendly, direct and practical. When a visitor describes a task, explain briefly how Konnect AI could automate it.
- Pricing and timelines depend on the project and are set in the written plan after the free call. Never quote prices, discounts or delivery dates, and never promise specific results or savings.
- If you don't know something, say so and suggest booking a call or emailing Tristan.
- When a visitor seems interested, suggest booking the free build call and include the booking link.
- Stay on topics related to Konnect AI, automation and websites. Politely decline unrelated requests.`;

const MAX_TURNS = 12;      // messages of history sent to the model
const MAX_CHARS = 1500;    // per message
const hits = new Map();    // simple per-instance rate limit: ip -> [timestamps]

function rateLimited(ip) {
  const now = Date.now(), win = 10 * 60 * 1000;
  const list = (hits.get(ip) || []).filter((t) => now - t < win);
  list.push(now); hits.set(ip, list);
  return list.length > 30;
}

const json = (status, body) =>
  new Response(JSON.stringify(body), { status, headers: { "content-type": "application/json" } });

export default async (req, context) => {
  if (req.method !== "POST") return json(405, { error: "Method not allowed" });
  if (!process.env.ANTHROPIC_API_KEY) return json(503, { error: "Chat is not configured yet." });
  if (rateLimited(context?.ip || "unknown")) return json(429, { error: "Too many messages. Please try again in a few minutes." });

  let body;
  try { body = await req.json(); } catch { return json(400, { error: "Invalid request." }); }

  const messages = (Array.isArray(body?.messages) ? body.messages : [])
    .filter((m) => (m?.role === "user" || m?.role === "assistant") && typeof m.content === "string" && m.content.trim())
    .slice(-MAX_TURNS)
    .map((m) => ({ role: m.role, content: m.content.slice(0, MAX_CHARS) }));
  while (messages.length && messages[0].role !== "user") messages.shift();
  if (!messages.length || messages[messages.length - 1].role !== "user") return json(400, { error: "Send a message to start." });

  try {
    const response = await client.beta.messages.create({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      output_config: { effort: "low" },
      betas: ["server-side-fallback-2026-07-01"],
      fallbacks: "default",
      cache_control: { type: "ephemeral" },
      system: SYSTEM,
      messages,
    });

    if (response.stop_reason === "refusal") {
      return json(200, { reply: "I can't help with that here. For anything about automation or websites, email tristan@getkonnectai.com or book a call: https://calendar.app.google/ZGPwJmMpcz3yWbkt5" });
    }
    const reply = response.content.filter((b) => b.type === "text").map((b) => b.text).join("\n").trim();
    return json(200, { reply: reply || "Sorry, I didn't catch that. Could you rephrase?" });
  } catch (error) {
    if (error instanceof Anthropic.RateLimitError) return json(429, { error: "We're busy right now. Please try again in a minute." });
    if (error instanceof Anthropic.AuthenticationError) { console.error("Chat: invalid ANTHROPIC_API_KEY"); return json(503, { error: "Chat is temporarily unavailable." }); }
    if (error instanceof Anthropic.APIError) { console.error(`Chat API error ${error.status}: ${error.message}`); return json(502, { error: "Chat is temporarily unavailable." }); }
    console.error("Chat error:", error);
    return json(500, { error: "Chat is temporarily unavailable." });
  }
};

export const config = { path: "/api/chat" };
