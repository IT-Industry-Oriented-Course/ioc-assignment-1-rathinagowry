from agent import run_agent

if __name__ == "__main__":
    query = (
        "Schedule a cardiology follow-up for patient Ravi Kumar "
        "next week and check insurance eligibility"
    )

    result = run_agent(query, dry_run=False)
    print(result)

# import argparse
# from agent import run_agent


# def main():
#     parser = argparse.ArgumentParser(description="Run clinical agent or serve API")
#     parser.add_argument("--serve", action="store_true", help="Start FastAPI server")
#     parser.add_argument("--host", default="0.0.0.0", help="Host for the API server")
#     parser.add_argument("--port", type=int, default=8000, help="Port for the API server")
#     parser.add_argument("--query", type=str, default=None, help="Run a single query and exit")
#     parser.add_argument("--dry-run", action="store_true", help="Run agent in dry-run mode")
#     args = parser.parse_args()

#     if args.serve:
#         try:
#             import uvicorn

#             uvicorn.run("api:app", host=args.host, port=args.port)
#         except Exception as e:
#             print(f"Failed to start server: {e}")
#         return

#     query = args.query or (
#         "Schedule a cardiology follow-up for patient Ravi Kumar "
#         "next week and check insurance eligibility"
#     )

#     result = run_agent(query, dry_run=args.dry_run)
#     print(result)


# if __name__ == "__main__":
#     main()
