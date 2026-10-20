import Foundation
import Vision
import CryptoKit

// Offline extraction only: never open, navigate to, or execute decoded payloads.
guard CommandLine.arguments.count == 2 else {
    FileHandle.standardError.write(Data("Usage: decode-qr IMAGE\n".utf8))
    exit(2)
}
do {
    let url = URL(fileURLWithPath: CommandLine.arguments[1])
    let bytes = try Data(contentsOf: url)
    let hash = SHA256.hash(data: bytes).map { String(format: "%02x", $0) }.joined()
    let request = VNDetectBarcodesRequest()
    request.symbologies = [.qr]
    // Decode exactly the bytes hashed above, even if the path changes meanwhile.
    try VNImageRequestHandler(data: bytes, options: [:]).perform([request])
    let payloads = (request.results ?? []).compactMap(\.payloadStringValue)
    let result: [String: Any] = [
        "source_sha256": hash,
        "method": "Apple Vision VNDetectBarcodesRequest, QR only, offline",
        "decoded_at": ISO8601DateFormatter().string(from: Date()),
        "payloads": payloads,
        "observations_count": request.results?.count ?? 0,
        "destinations_opened": false
    ]
    let data = try JSONSerialization.data(withJSONObject: result, options: [.prettyPrinted, .sortedKeys])
    FileHandle.standardOutput.write(data)
    FileHandle.standardOutput.write(Data("\n".utf8))
} catch {
    FileHandle.standardError.write(Data("QR extraction failed: \(error)\n".utf8))
    exit(1)
}
