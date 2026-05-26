import type { NextConfig } from "next";

const nextConfig: NextConfig = {
 async rewrites() {
    return [
      {
        // Cualquier petición que haga el frontend a /api/algo...
        source: '/api/:path*',
        // ...se redirige en secreto al puerto 5328 de FastAPI
        destination: 'http://127.0.0.1:5328/api/:path*',
      },
    ]
  },
};

export default nextConfig;
