"""Step 2: upload the pages to S3 and index them into the Knowledge Base.

An ingestion job reads the bucket, chunks each page, embeds the chunks
and writes the vectors. Re-running it only re-indexes changed files.
"""
import sys
import time

from common import PAGES, ROOT, client, outputs


def main() -> int:
    out = outputs()
    pages = sorted(p for p in PAGES.glob("*") if p.name != "README.md")
    if not pages:
        print("No pages found. Run scripts/01_fetch_pages.py first.")
        return 1

    s3 = client("s3")
    for path in pages:
        ctype = "application/json" if path.suffix == ".json" else "text/markdown"
        s3.upload_file(str(path), out["docs_bucket"], f"pages/{path.name}", ExtraArgs={"ContentType": ctype})
    print(f"uploaded {len(pages)} files to s3://{out['docs_bucket']}/pages/")

    agent = client("bedrock-agent")
    ids = {"knowledgeBaseId": out["knowledge_base_id"], "dataSourceId": out["data_source_id"]}
    job = agent.start_ingestion_job(**ids)["ingestionJob"]
    while job["status"] not in ("COMPLETE", "FAILED", "STOPPED"):
        time.sleep(5)
        job = agent.get_ingestion_job(**ids, ingestionJobId=job["ingestionJobId"])["ingestionJob"]
        print(f"  ingestion: {job['status']}")
    s = job.get("statistics", {})
    print(f"scanned {s.get('numberOfDocumentsScanned')}, indexed {s.get('numberOfNewDocumentsIndexed')} new, "
          f"{s.get('numberOfModifiedDocumentsIndexed')} modified, {s.get('numberOfDocumentsFailed')} failed")
    for reason in job.get("failureReasons", []):
        print("  reason:", reason)
    if job["status"] != "COMPLETE" or s.get("numberOfDocumentsFailed"):
        return 1

    # Quick retrieval check, with no LLM involved.
    hits = client("bedrock-agent-runtime").retrieve(
        knowledgeBaseId=out["knowledge_base_id"],
        retrievalQuery={"text": "When are exam results released?"},
        retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": 3}},
    )["retrievalResults"]
    print("\nretrieval check: 'When are exam results released?'")
    for h in hits:
        print(f"  {h.get('score', 0):.3f}  {h.get('metadata', {}).get('source_url', '')}\n         {h['content']['text'][:110]!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
