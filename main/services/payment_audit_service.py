from main.models import PaymentAudit


class PaymentAuditService:

    @staticmethod
    def create(

        *,

        payment,

        provider,

        endpoint,

        ip_address,

        user_agent,

        request_headers,

        request_body,

        response_body,

        status,

        error="",

        duration_ms=0,

    ):

        return PaymentAudit.objects.create(

            payment=payment,

            provider=provider,

            endpoint=endpoint,

            ip_address=ip_address,

            user_agent=user_agent,

            request_headers=request_headers,

            request_body=request_body,

            response_body=response_body,

            status=status,

            error=error,

            duration_ms=duration_ms,

        )