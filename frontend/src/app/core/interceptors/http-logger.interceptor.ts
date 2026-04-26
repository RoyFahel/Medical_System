import { HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, finalize, throwError } from 'rxjs';

@Injectable()
export class HttpLoggerInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const start = performance.now();

    // eslint-disable-next-line no-console
    console.debug('[HTTP]', req.method, req.urlWithParams, this.summarizeBody(req.body));

    return next.handle(req).pipe(
      catchError((err: unknown) => {
        // eslint-disable-next-line no-console
        console.error('[HTTP ERROR]', req.method, req.urlWithParams, err);
        return throwError(() => err);
      }),
      finalize(() => {
        const ms = Math.round(performance.now() - start);
        // eslint-disable-next-line no-console
        console.debug('[HTTP DONE]', req.method, req.urlWithParams, `${ms}ms`);
      })
    );
  }

  private summarizeBody(body: unknown): unknown {
    if (!body) return body;
    if (body instanceof FormData) {
      const out: Record<string, unknown> = {};
      body.forEach((value, key) => {
        if (value instanceof File) out[key] = `[File name=${value.name} size=${value.size}]`;
        else out[key] = value;
      });
      return out;
    }
    if (body instanceof Blob) return `[Blob size=${body.size}]`;
    return body;
  }
}

