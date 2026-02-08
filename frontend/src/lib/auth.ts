import { betterAuth } from "better-auth";
import { Pool } from "@neondatabase/serverless";

const databaseUrl = process.env.DATABASE_URL;

function getBaseURL() {
  if (process.env.BETTER_AUTH_URL) return process.env.BETTER_AUTH_URL;
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`;
  return "http://localhost:3000";
}

export const auth = betterAuth({
  database: databaseUrl
    ? new Pool({ connectionString: databaseUrl })
    : { provider: "sqlite" as const, url: "file:./auth.db" },
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
