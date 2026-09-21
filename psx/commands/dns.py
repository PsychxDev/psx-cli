import socket
import sys

from psx.utils.display import header, sep


def normalize_hostname(value: str) -> str:
    if not value:
        raise ValueError("Domain input is empty.")

    host = str(value).strip().rstrip(".").lower()
    if not host or " " in host:
        raise ValueError(f"Invalid domain input: {value}")
    if host.startswith("http://") or host.startswith("https://"):
        try:
            host = host.split("//", 1)[1].split("/", 1)[0]
        except IndexError as exc:
            raise ValueError(f"Invalid domain input: {value}") from exc
    return host


def lookup_dns(domain: str) -> dict:
    host = normalize_hostname(domain)
    records = {
        "domain": host,
        "a_records": [],
        "aaaa_records": [],
        "status": "ok",
        "reachable": True,
        "error": None,
    }

    try:
        for result in socket.getaddrinfo(host, None, type=socket.SOCK_STREAM):
            family, _, _, _, sockaddr = result
            ip = sockaddr[0]
            if family == socket.AF_INET and ip not in records["a_records"]:
                records["a_records"].append(ip)
            elif family == socket.AF_INET6 and ip not in records["aaaa_records"]:
                records["aaaa_records"].append(ip)
    except (socket.gaierror, OSError):
        records["status"] = "error"
        records["reachable"] = False
        records["error"] = f"DNS lookup failed for {host}"

    return records


def run(target: str = None) -> None:
    host = target or (sys.argv[2] if len(sys.argv) > 2 else None)
    length = header("DNS")

    if not host:
        print("Usage: psx dns <domain>")
        sep(length)
        return

    result = lookup_dns(host)
    print(f"{'Domain:':9} {result['domain']}")
    print(f"{'A:':9} {', '.join(result['a_records']) if result['a_records'] else 'Not available'}")
    print(f"{'AAAA:':9} {', '.join(result['aaaa_records']) if result['aaaa_records'] else 'Not available'}")

    if not result["reachable"]:
        print(f"{'Status:':9} {result['status']}")
        print(f"{'Error:':9} {result['error']}")
    else:
        print(f"{'Status:':9} OK")

    sep(length)
