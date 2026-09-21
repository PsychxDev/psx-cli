import socket
import sys
import time
from difflib import get_close_matches
from urllib.parse import urlsplit

from psx.utils.display import header, sep

COMMON_DOMAINS = [
    "github.com",
    "gitlab.com",
    "google.com",
    "microsoft.com",
    "amazon.com",
    "facebook.com",
    "example.com",
    "python.org",
    "wikipedia.org",
    "duckduckgo.com",
    "github.io",
    "outlook.com",
    "netflix.com",
]


class DomainLookupError(RuntimeError):
    def __init__(self, message: str, kind: str = "error"):
        super().__init__(message)
        self.message = message
        self.kind = kind


def normalize_domain(value: str) -> str:
    if value is None:
        raise ValueError("Domain input is empty.")

    raw = str(value).strip()
    if not raw:
        raise ValueError("Domain input is empty.")

    if "//" in raw or raw.lower().startswith(("http://", "https://")):
        try:
            hostname = urlsplit(raw).hostname
        except ValueError as exc:
            raise ValueError(f"Invalid URL: {raw}") from exc
        if not hostname:
            raise ValueError(f"Invalid URL: {raw}")
        normalized = hostname.rstrip(".").lower()
    else:
        if "/" in raw or "?" in raw or "#" in raw:
            try:
                hostname = urlsplit(f"//{raw}").hostname
            except ValueError as exc:
                raise ValueError(f"Invalid domain input: {raw}") from exc
            if not hostname:
                raise ValueError(f"Invalid domain input: {raw}")
            normalized = hostname.rstrip(".").lower()
        else:
            normalized = raw.rstrip(".").lower().strip()

    if not normalized or any(ch.isspace() for ch in normalized):
        raise ValueError(f"Invalid domain input: {raw}")

    if not validate_domain(normalized):
        raise ValueError(f"Invalid domain input: {raw}")

    return normalized


def validate_domain(domain: str) -> bool:
    if not domain:
        return False

    host = domain.strip().rstrip(".").lower()
    if not host or host == "localhost":
        return False
    if host.startswith(".") or host.endswith("."):
        return False
    if any(ch.isspace() for ch in host):
        return False
    if ":" in host:
        return False
    if len(host) > 253:
        return False

    try:
        socket.inet_pton(socket.AF_INET, host)
        return False
    except OSError:
        pass

    try:
        socket.inet_pton(socket.AF_INET6, host)
        return False
    except OSError:
        pass

    labels = host.split(".")
    if len(labels) < 2:
        return False
    if any(label == "" for label in labels):
        return False

    for label in labels:
        if len(label) > 63 or len(label) < 1:
            return False
        if label.startswith("-") or label.endswith("-"):
            return False
        if not all(char.isalnum() or char == "-" for char in label):
            return False

    if len(labels[-1]) < 2:
        return False

    return True


def resolve_domain(domain: str) -> dict:
    normalized = normalize_domain(domain)
    if not validate_domain(normalized):
        raise ValueError(f"Invalid domain: {normalized}")

    addresses = []
    ipv4 = []
    ipv6 = []

    try:
        for result in socket.getaddrinfo(normalized, None, type=socket.SOCK_STREAM):
            family, _, _, _, sockaddr = result
            address = sockaddr[0]
            if address and address not in addresses:
                addresses.append(address)
                if family == socket.AF_INET:
                    ipv4.append(address)
                elif family == socket.AF_INET6:
                    ipv6.append(address)
    except socket.gaierror as exc:
        if exc.errno in (socket.EAI_NONAME, socket.EAI_NODATA):
            raise DomainLookupError(f"Domain '{normalized}' does not resolve.", kind="not_found") from exc
        raise DomainLookupError(f"DNS/network lookup failed for '{normalized}'.", kind="network") from exc
    except OSError as exc:
        raise DomainLookupError(f"DNS/network lookup failed for '{normalized}'.", kind="network") from exc

    return {
        "domain": normalized,
        "addresses": sorted(addresses),
        "ipv4": sorted(ipv4),
        "ipv6": sorted(ipv6),
        "status": "resolved",
    }


def check_web_service(hostname: str, timeout: float = 1.0) -> dict:
    results = {}
    for port in (80, 443):
        try:
            with socket.create_connection((hostname, port), timeout=timeout):
                results[port] = {
                    "port": port,
                    "status": "Open",
                    "reachable": True,
                }
        except socket.timeout:
            results[port] = {
                "port": port,
                "status": "Timeout",
                "reachable": False,
            }
        except ConnectionRefusedError:
            results[port] = {
                "port": port,
                "status": "Closed",
                "reachable": False,
            }
        except OSError as exc:
            results[port] = {
                "port": port,
                "status": "Error",
                "reachable": False,
                "detail": str(exc),
            }
    return results


def suggest_domains(domain: str, limit: int = 5) -> list[str]:
    if not domain:
        return []

    target = normalize_domain(domain) if domain else domain.strip().rstrip(".").lower()
    if not target or target == "localhost":
        return []

    try:
        matches = get_close_matches(target, COMMON_DOMAINS, n=limit, cutoff=0.45)
    except Exception:
        matches = []

    if not matches:
        base = target.split(".")[-2:] if "." in target else [target]
        fallback = [".".join(base), "example.com"]
        matches = [item for item in fallback if item != target][:limit]

    return [item for item in matches if item != target][:limit]


def prompt_selection(options: list[str]) -> str | None:
    if not options:
        return None

    print("Similar domains:")
    for index, option in enumerate(options, start=1):
        print(f"  {index}. {option}")

    while True:
        try:
            choice = input(f"Select a domain [1-{len(options)}]: ").strip()
        except EOFError:
            print()
            print("Selection cancelled.")
            return None
        except KeyboardInterrupt:
            print()
            print("Selection cancelled.")
            return None

        if not choice:
            print("Please enter a number from the list.")
            continue

        if choice.isdigit():
            number = int(choice)
            if 1 <= number <= len(options):
                return options[number - 1]

        print("Invalid selection. Please choose a valid number.")


def lookup_domain(target: str) -> dict:
    normalized = normalize_domain(target)
    if not validate_domain(normalized):
        raise ValueError(f"Invalid domain input: {normalized}")

    try:
        resolution = resolve_domain(normalized)
    except DomainLookupError as exc:
        suggestions = suggest_domains(normalized)
        if suggestions:
            selected = prompt_selection(suggestions)
            if selected:
                return lookup_domain(selected)
            return {"domain": normalized, "status": "suggestion_cancelled", "error": exc.message}
        raise DomainLookupError(exc.message, kind=exc.kind) from exc

    web_services = check_web_service(normalized)
    resolution["web_services"] = web_services
    return resolution


def show_loading(message: str, steps: int = 10) -> None:
    frames = ["|", "/", "-", "\\"]
    for index in range(steps):
        frame = frames[index % len(frames)]
        sys.stdout.write(f"\r{message} {frame}")
        sys.stdout.flush()
        time.sleep(0.08)
    sys.stdout.write("\r" + " " * (len(message) + 6) + "\r")
    sys.stdout.flush()


def clear_loading() -> None:
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.flush()


def summarize_lookup(result: dict) -> str:
    domain = result.get("domain", "unknown")
    ipv4 = result.get("ipv4", [])
    ipv6 = result.get("ipv6", [])
    web_services = result.get("web_services", {})
    http_status = web_services.get(80, {}).get("status", "Unknown")
    https_status = web_services.get(443, {}).get("status", "Unknown")

    summary = (
        f"Summary: {domain} resolved to {len(ipv4)} IPv4 and {len(ipv6)} IPv6 addresses. "
        f"HTTP={http_status}, HTTPS={https_status}."
    )
    return summary


def run(target: str = None) -> None:
    if target is None:
        args = sys.argv[2:]
        target = args[0] if args else None

    if not target:
        length = header("Domain Lookup")
        print("Usage: psx domain <domain-or-url>")
        sep(length)
        return

    length = header("Domain Lookup")
    show_loading("Resolving domain")
    clear_loading()

    try:
        result = lookup_domain(target)
    except ValueError as exc:
        print(f"[!] Invalid domain input: {exc}")
        sep(length)
        return
    except DomainLookupError as exc:
        if exc.kind == "not_found":
            print(f"[!] {exc.message}")
            suggestions = suggest_domains(target)
            if suggestions:
                print("Similar domains:")
                for index, suggestion in enumerate(suggestions, start=1):
                    print(f"  {index}. {suggestion}")
                selected = prompt_selection(suggestions)
                if selected:
                    try:
                        target = selected
                        show_loading("Resolving selected domain")
                        clear_loading()
                        result = lookup_domain(target)
                    except (ValueError, DomainLookupError) as retry_error:
                        print(f"[!] {retry_error}")
                        sep(length)
                        return
                else:
                    sep(length)
                    return
            else:
                print("Suggestions are unavailable for this domain.")
        else:
            print(f"[!] {exc.message}")
        sep(length)
        return

    print(f"{'Domain:':12} {result['domain']}")
    print("DNS")
    if result.get("ipv4"):
        print(f"  {'IPv4:':12} {', '.join(result['ipv4'])}")
    else:
        print(f"  {'IPv4:':12} Not available")

    if result.get("ipv6"):
        print(f"  {'IPv6:':12} {', '.join(result['ipv6'])}")
    else:
        print(f"  {'IPv6:':12} Not available")

    print("Web Services")
    for port in (80, 443):
        status = result.get("web_services", {}).get(port, {}).get("status", "Error")
        port_name = "HTTP" if port == 80 else "HTTPS"
        print(f"  {port_name:<6}: {status}")

    print()
    print(summarize_lookup(result))
    sep(length)
