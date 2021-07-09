#' ---
#' title: "Notes on Explore Program WRDS with R"
#' date:  "`r Sys.Date()`"
#' author: Chris Zheng
#' email: chrizheng@vip.sina.com.cn
#' output:
#'   html_document:
#'      fig_caption: yes
#'      number_sections: yes
#'      toc: yes
#'      toc_depth: 4
#'      toc_float:
#'        collapsed: no
#'        smooth_scroll: no
#'      df_print: paged
#'      theme: cerulean
#'      highlight: pygments
#' ---


#' # Exploring database from WRDS

#' ## Connect with WRDS

#+ connect_wrds

library(DBI)

# Connect with WRDS database with my account
con_wrds <- dbConnect(RPostgres::Postgres(),
                  host = "wrds-pgdata.wharton.upenn.edu",
                  port = 9737,
                  dbname = "wrds",
                  sslmode = "require",
                  user = "cz2003"
)
withr::defer(
  dbDisconnect(con_wrds)
)

table_list <- dbListTables(con_wrds)
df.table_list <- tibble::tibble(table_name = table_list)

dbListFields(con_wrds, "dsf")

dbReadTable(con_wrds, "dsf")
