#
# NOTICE:
#  This file contains views created during 'db-init'.
#

views = []

views.append(
    [
        "media",
        {
            "_id": "_design/filters",
            "views": {
                "names": {
                    "map": "function(doc) { \n  emit(doc._id, [doc.directory, doc.play.status, doc.play.rating, doc.play.rating_notes, doc.play.notes, doc.sources, doc.metadata.duration]);\n}"
                },
                "stats_status": {
                    "map": "function (doc) {\n  emit(doc.play.status, 1);\n}",
                    "reduce": "_count",
                },
                "stats_total": {
                    "map": "function (doc) {\n  emit(doc._id, 1);\n}",
                    "reduce": "_count",
                },
                "stats_sources": {
                    "reduce": "_count",
                    "map": "function (doc) {\n  emit(doc.sources, 1);\n}",
                },
            },
        },
    ]
)

views.append(
    [
        "injest_logs",
        {
            "_id": "_design/filters",
            "views": {
                "status": {
                    "map": "function (doc) {\n  emit([doc.batchid, doc.status, doc.reason], 1);\n}",
                    "reduce": "_count",
                }
            },
            "language": "javascript",
        },
    ]
)
