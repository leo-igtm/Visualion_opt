import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async redirects() {
    return [
      {
                // Requests to /api/<path> will be sent to the FastAPI server

        source: "/api/:path*",
        destination: "http://127.0.0.1:5328/api/:path*",
        permanent: false,
      },
    ];
  }
};

export default nextConfig;
