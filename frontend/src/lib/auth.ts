import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { drizzle } from "drizzle-orm/neon-http";
import { neon } from "@neondatabase/serverless";

const databaseUrl = process.env.DATABASE_URL;

function getBaseURL() {
  if (process.env.BETTER_AUTH_URL) return process.env.BETTER_AUTH_URL;
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`;
  return "http://localhost:3000";
}

function getDatabase() {
  if (!databaseUrl) {
    // Fallback for build time when DATABASE_URL is not set
    return { provider: "sqlite" as const, url: "file:./auth.db" };
  }
  const sql = neon(databaseUrl);
  const db = drizzle({ client: sql });
  return drizzleAdapter(db, {
    provider: "pg",
    transaction: false, // Neon HTTP doesn't support transactions
  });
}

export const auth = betterAuth({
  database: getDatabase(),
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
  },
  secret: process.env.BETTER_AUTH_SECRET,
  baseURL: getBaseURL(),
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    cookieCache: {
      enabled: true,
      maxAge: 60 * 5, // 5 minutes
    },
  },
  trustedOrigins: [
    getBaseURL(),
    process.env.VERCEL_URL ? `https://${process.env.VERCEL_URL}` : "",
  ].filter(Boolean),
});
