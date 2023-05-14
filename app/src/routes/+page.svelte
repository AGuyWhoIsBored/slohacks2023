<script lang="ts">
	let enteredClasses: string;

	$: console.log('classes', enteredClasses);
</script>

<div class="appContainer m-4">
	<div class="card cardStyles h-full">
		<div class="card-body">
			<div>
				<h1 class="text-3xl font-medium inline-block">Cal Poly Curriculum Sheet Validator</h1>
				<img
					class="inline-block ml-2 mb-2"
					src="/logo.png"
					width="32"
					height="32"
					alt="horse thing"
				/>
			</div>

			<div class="flex justify-between">
				<p class="flex-grow-0">How does this work? It doesn't</p>
				<p class="flex-grow-0">
					Duncan Applegarth, Mitchell Kanazawa, Wesley Kwok (SLO Hacks 2023)
				</p>
			</div>

			<div class="flex w-full flex-grow">
				<div class="grid flex-grow">
					<div>
						<div>
							<h2 class="text-center text-2xl font-medium mt-4">Enter Classes Here</h2>
							<div class="divider mx-8 h-0" />
						</div>
						<textarea
							class="w-full h-72 resize-none border-2"
							placeholder="Enter your courses here, one on each line"
							bind:value={enteredClasses}
						/>
					</div>
				</div>
				<div class="divider divider-horizontal" />
				<div class="grid flex-grow">
					<div>
						<h2 class="text-center text-2xl font-medium mt-4">Validation Results</h2>
						<div class="divider mx-8 h-0" />
					</div>
				</div>
			</div>
		</div>
	</div>
</div>

<style lang="postcss">
	.appContainer {
		/* got lazy */
		height: calc(100vh - 32px);
	}

	.cardStyles {
		@apply shadow border-base-300 rounded-sm;

		/* make shadow a hair darker */
		--tw-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.2), 0 1px 2px 0 rgba(0, 0, 0, 0.16);
	}
</style>
