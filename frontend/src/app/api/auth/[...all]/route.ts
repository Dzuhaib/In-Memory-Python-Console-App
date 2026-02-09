import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";
import { NextRequest, NextResponse } from "next/server";

const { POST: _POST, GET: _GET } = toNextJsHandler(auth);

export async function POST(req: NextRequest) {
  try {
    return await _POST(req);
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : String(error);
    const stack = error instanceof Error ? error.stack : undefined;
    console.error("Better Auth POST error:", message, stack);
    return NextResponse.json(
      { error: message, detail: stack?.split("\n").slice(0, 5) },
      { status: 500 }
    );
  }
}

export async function GET(req: NextRequest) {
  try {
    return await _GET(req);
  } catch (error: unknown) {
    const message = error instanceof Error ? error.message : String(error);
    console.error("Better Auth GET error:", message);
    return NextResponse.json(
      { error: message },
      { status: 500 }
    );
  }
}
