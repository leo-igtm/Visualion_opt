'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { oauthFrontendService } from '@/lib/auth/oauth';

export default function GoogleCallbackPage() {
    const router = useRouter();
    const searchParams = useSearchParams();
    const [status, setStatus] = useState('Verificando cuenta...');

    useEffect(() => {
        const code = searchParams.get('code');
        if (!code) {
            setStatus('Error: No se recibió código de autenticación.');
            setTimeout(() => router.push('/login'), 3000);
            return;
        }

        const procesarAuth = async () => {
            try {
                await oauthFrontendService.handleGoogleCallback(code);
                setStatus('¡Autenticación exitosa! Redirigiendo...');
                setTimeout(() => router.push('/dashboard'), 1500);
            } catch (error) {
                console.error(error);
                setStatus('Error al autenticar con Google.');
                setTimeout(() => router.push('/login'), 3000);
            }
        };

        procesarAuth();
    }, [router, searchParams]);

    return (
        <div className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 flex flex-col items-center justify-center">
            <div className="w-12 h-12 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin mb-4"></div>
            <h2 className="text-xl font-medium text-gray-200">{status}</h2>
        </div>
    );
}
