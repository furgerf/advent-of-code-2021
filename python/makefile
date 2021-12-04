DAY=

.PHONY: prepare-day

prepare-day:
ifndef DAY
	$(error Must specify DAY)
endif
	@mkdir -p day_$(DAY)
	@cp day_template.py day_$(DAY)/day_$(DAY).py
	@sed -i 's/XXX/$(DAY)/g' day_$(DAY)/day_$(DAY).py
	@xclip -o > day_$(DAY)/input
	@echo "Number of input lines: $$(wc -l day_$(DAY)/input | cut -d' ' -f 1)"
	@head day_$(DAY)/input

